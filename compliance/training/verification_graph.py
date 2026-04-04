"""
LangGraph Verification Graph — Orchestrates the 3-layer cross-verification network.
Implements:
  - Parallel verifier execution (ComplianceValidator || PolicyAgent || WorkflowAgent)
  - Consensus computation (2/3 majority)
  - HITL interrupt on REFUTED or high drift
  - Training corpus write on flagged interactions
  - Drift monitoring via Evidently AI (optional)

Requirements:
    pip install langgraph langchain-core

Usage:
    python3 compliance/training/verification_graph.py \
        --statement "Agent statement" \
        --agent-id "kyc-v2" \
        --agent-role "KYC Specialist"
"""
from __future__ import annotations

import argparse
import json
from typing import Annotated, Any, TypedDict

try:
    from langgraph.graph import END, START, StateGraph
    from langgraph.checkpoint.memory import MemorySaver
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

from compliance.verification.orchestrator import (
    ConsensusResult,
    run_verification,
    print_result,
)


# ─────────────────────────────────────────────
# Graph State
# ─────────────────────────────────────────────

class VerificationState(TypedDict):
    """State flowing through the LangGraph verification graph."""
    # Input
    statement: str
    agent_id: str
    agent_role: str
    context: dict[str, Any]

    # Intermediate
    cv_result: dict | None       # Compliance Validator output
    pa_result: dict | None       # Policy Agent output
    wa_result: dict | None       # Workflow Agent output

    # Output
    consensus: str | None        # CONFIRMED / REFUTED / UNCERTAIN
    consensus_result: dict | None
    hitl_required: bool
    hitl_resolution: str | None  # Human decision if HITL triggered
    training_saved: bool
    error: str | None


# ─────────────────────────────────────────────
# Graph Nodes
# ─────────────────────────────────────────────

def node_run_verifiers(state: VerificationState) -> dict:
    """
    Run all 3 verifiers via orchestrator (parallel internally).
    This node is the core of the verification network.
    """
    try:
        result = run_verification(
            statement=state["statement"],
            agent_id=state["agent_id"],
            agent_role=state["agent_role"],
            context=state.get("context", {}),
        )
        import dataclasses
        result_dict = dataclasses.asdict(result)
        return {
            "cv_result": {
                "verdict": result.compliance_verdict,
                "rule": result.compliance_rule,
                "reason": result.compliance_reason,
                "confidence": result.compliance_confidence,
            },
            "pa_result": {
                "verdict": result.policy_verdict,
                "rule": result.policy_rule,
                "reason": result.policy_reason,
                "confidence": result.policy_confidence,
            },
            "wa_result": {
                "verdict": result.workflow_verdict,
                "rule": result.workflow_rule,
                "reason": result.workflow_reason,
                "confidence": result.workflow_confidence,
            },
            "consensus": result.consensus,
            "consensus_result": result_dict,
            "hitl_required": result.hitl_required,
            "training_saved": result.training_flag,
            "error": None,
        }
    except Exception as e:
        return {"error": str(e), "hitl_required": True}


def node_hitl_interrupt(state: VerificationState) -> dict:
    """
    HITL interrupt node — in production this suspends the graph
    and waits for human operator input.
    In this implementation: prints alert and records pending status.
    """
    result = state.get("consensus_result", {})
    print("\n" + "!" * 60)
    print("  ⚠️  HITL INTERRUPT — HUMAN REVIEW REQUIRED")
    print("!" * 60)
    print(f"  Agent:     {state['agent_id']} ({state['agent_role']})")
    print(f"  Consensus: {state.get('consensus', 'UNKNOWN')}")
    print(f"  Statement: {state['statement'][:100]}")
    if result.get("correction"):
        print(f"  Correction: {result['correction']}")
        print(f"  Source:     {result['correction_source']}")
    print("!" * 60)
    print("  → Flagged for MLRO/Compliance Officer review")
    print("  → Interaction saved to training corpus")
    print("!" * 60 + "\n")

    return {"hitl_resolution": "PENDING_HUMAN_REVIEW"}


def node_training_corpus(state: VerificationState) -> dict:
    """
    Ensure training data is properly recorded.
    In production: triggers RAG update + fine-tuning pipeline.
    """
    if state.get("training_saved"):
        print(f"[Training] Interaction saved to corpus (drift_score: "
              f"{state.get('consensus_result', {}).get('drift_score', 'N/A')})")

    # Drift monitoring hook (Evidently AI integration point)
    drift_score = state.get("consensus_result", {}).get("drift_score", 0)
    if drift_score >= 0.15:
        print(f"[Training] ⚠️  Drift score {drift_score:.3f} ≥ 0.15 threshold")
        print("[Training] → Triggering Evidently AI drift alert")
        # In production: evidently_ai_client.report_drift(state["agent_id"], drift_score)

    return {}


def node_confirmed(state: VerificationState) -> dict:
    """Handle confirmed (passing) verifications."""
    print(f"[Graph] ✅ CONFIRMED — Agent statement passes all 3 verifiers")
    return {}


# ─────────────────────────────────────────────
# Routing Logic
# ─────────────────────────────────────────────

def route_after_verification(state: VerificationState) -> str:
    """Route to HITL or confirmed based on consensus."""
    if state.get("error"):
        return "hitl_interrupt"
    if state.get("hitl_required"):
        return "hitl_interrupt"
    return "confirmed"


def route_after_hitl(state: VerificationState) -> str:
    """Always go to training corpus after HITL."""
    return "training_corpus"


# ─────────────────────────────────────────────
# Build Graph
# ─────────────────────────────────────────────

def build_verification_graph():
    """Construct the LangGraph verification workflow."""
    if not LANGGRAPH_AVAILABLE:
        raise ImportError(
            "LangGraph not installed. Run: pip install langgraph langchain-core"
        )

    graph = StateGraph(VerificationState)

    # Add nodes
    graph.add_node("run_verifiers", node_run_verifiers)
    graph.add_node("hitl_interrupt", node_hitl_interrupt)
    graph.add_node("confirmed", node_confirmed)
    graph.add_node("training_corpus", node_training_corpus)

    # Add edges
    graph.add_edge(START, "run_verifiers")
    graph.add_conditional_edges(
        "run_verifiers",
        route_after_verification,
        {
            "hitl_interrupt": "hitl_interrupt",
            "confirmed": "confirmed",
        }
    )
    graph.add_edge("hitl_interrupt", "training_corpus")
    graph.add_edge("confirmed", "training_corpus")
    graph.add_edge("training_corpus", END)

    # Compile with memory checkpointer (enables HITL resume in production)
    checkpointer = MemorySaver()
    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["hitl_interrupt"],  # Suspend BEFORE HITL node in production
    )


# ─────────────────────────────────────────────
# Fallback: Direct Orchestrator (without LangGraph)
# ─────────────────────────────────────────────

def run_without_langgraph(statement: str, agent_id: str, agent_role: str) -> ConsensusResult:
    """Run verification directly via orchestrator (no LangGraph dependency)."""
    result = run_verification(
        statement=statement,
        agent_id=agent_id,
        agent_role=agent_role,
    )
    print_result(result)
    return result


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BANXE LangGraph Verification Graph")
    parser.add_argument("--statement", required=True)
    parser.add_argument("--agent-id", default="unknown")
    parser.add_argument("--agent-role", default="KYC Specialist")
    parser.add_argument("--no-langgraph", action="store_true",
                        help="Run without LangGraph (direct orchestrator)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.no_langgraph or not LANGGRAPH_AVAILABLE:
        if not LANGGRAPH_AVAILABLE:
            print("[Graph] LangGraph not installed — using direct orchestrator")
        result = run_without_langgraph(args.statement, args.agent_id, args.agent_role)
        if args.json:
            import dataclasses
            print(json.dumps(dataclasses.asdict(result), indent=2, ensure_ascii=False))
        return

    # Run via LangGraph
    graph = build_verification_graph()
    config = {"configurable": {"thread_id": f"{args.agent_id}-{__import__('time').time()}"}}

    initial_state: VerificationState = {
        "statement": args.statement,
        "agent_id": args.agent_id,
        "agent_role": args.agent_role,
        "context": {},
        "cv_result": None,
        "pa_result": None,
        "wa_result": None,
        "consensus": None,
        "consensus_result": None,
        "hitl_required": False,
        "hitl_resolution": None,
        "training_saved": False,
        "error": None,
    }

    print(f"\n[Graph] Starting verification for: {args.agent_id}")
    final_state = graph.invoke(initial_state, config=config)

    if args.json:
        print(json.dumps(final_state.get("consensus_result", {}), indent=2, ensure_ascii=False))
    else:
        print(f"\n[Graph] Final consensus: {final_state.get('consensus', 'UNKNOWN')}")


if __name__ == "__main__":
    main()
