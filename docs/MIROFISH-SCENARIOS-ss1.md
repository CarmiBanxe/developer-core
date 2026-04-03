# docs/MIROFISH-SCENARIOS.md — SS1 Legal Case Management

**Project:** ss1  
**Type:** Legal/Appeal Dynamics  
**MiroFish Role:** Appellate procedure & case strategy validation  
**Auto-trigger:** Appeal keywords (апелляция, пересмотр, кассация)

---

## Scenario Library

### 1. Appeal Dynamics Simulation (`appeal-dynamics.yml`)

**Purpose:** Model appellate court process from filing to decision

**Triggers:** `appeal`, `апелляция`, `notice of appeal`, `appellate brief`

**Timeline:**
```
Day 0:   Trial court final judgment
Day 30:  Notice of Appeal filed (deadline: 30 days)
Day 60:  Designation of Record (clerk compiles trial documents)
Day 90:  Appellant's Opening Brief due
Day 120: Appellee's Response Brief due
Day 150: Appellant's Reply Brief due
Day 180: Oral Argument (if granted)
Day 240: Decision expected (3-6 months total)
```

**Agents:**
- **Appellant Attorney:** Challenging the ruling
- **Appellee Attorney:** Defending the judgment
- **Appellate Judge #1:** Legal scholar focus
- **Appellate Judge #2:** Pragmatic impact focus
- **Appellate Judge #3:** Procedural strictness focus
- **Law Clerk:** Research & memo drafting

**Brief Writing Simulation:**

**Appellant's Opening Brief (40 pages max):**
```
Issue Presented:
"Whether trial court erred in granting summary judgment when genuine dispute of material fact existed regarding contract modification."

Statement of Facts:
- Favorable to appellant but accurate
- Citations to record (deposition p.45, email Ex.C)
- No argumentation (save for Argument section)

Argument (IRAC format):
Issue: Did trial court err?
Rule: Summary judgment standard (genuine dispute test)
Analysis: Evidence creates factual question for jury
Conclusion: Reverse and remand for trial

Relief Requested:
"Reverse summary judgment and remand for trial on merits."
```

**Appellee's Response Strategy:**
- Waiver arguments (issues not preserved at trial)
- Standard of attack (abuse of discretion = hard to reverse)
- Alternative grounds (affirm on different legal theory)
- Sanctions threat (frivolous appeal?)

**Oral Argument Prep:**
- 15 minutes per side
- Judge interruptions every 60-90 seconds
- Hot bench (judges read briefs thoroughly)
- Focus on weakest points in each argument

**Decision Outcomes:**
- **Affirm:** Trial court upheld (40% of appeals)
- **Reverse:** Trial court overturned (25%)
- **Remand:** Sent back for further proceedings (30%)
- **Dismiss:** Procedural defect (5%)

---

### 2. Case Strategy Permutation (`case-permutation.yml`)

**Purpose:** Evaluate multiple litigation strategies simultaneously

**Triggers:** `case permutation`, `strategy options`, `alternative approach`

**Base Case:** Contract dispute (£500k damages)

**Strategy A (Aggressive Litigation):**
- File immediately in High Court
- Seek summary judgment
- Motion for preliminary injunction
- Timeline: 12-18 months
- Cost: £150k-£250k
- Win probability: 55%
- Recovery: £300k net (after costs)

**Strategy B (Negotiation-First):**
- Demand letter with 30-day response
- Mediation before filing
- File only if settlement fails
- Timeline: 6-9 months
- Cost: £30k-£50k
- Settlement probability: 70%
- Recovery: £200k net (average settlement)

**Strategy C (Arbitration Clause):**
- Invoke contractual arbitration
- Select arbitrator (industry expert)
- Faster than court, private
- Timeline: 6-8 months
- Cost: £80k-£120k (arbitrator fees split)
- Win probability: 60% (expert decision-maker)
- Recovery: £350k net

**Strategy D (Regulatory Complaint):**
- File FCA complaint parallel to civil case
- Regulatory pressure forces settlement
- Risk: FCA investigation expands scope
- Timeline: 9-15 months
- Cost: £50k-£100k
- Settlement probability: 80%
- Recovery: £250k net

**Simulation Output:**
| Strategy | NPV (Net Present Value) | Risk Score | Recommendation |
|----------|------------------------|------------|----------------|
| A | £180k | High (7/10) | Only if defendant judgment-proof |
| B | £165k | Low (3/10) | ✅ Best risk-adjusted return |
| C | £210k | Medium (5/10) | Preferred if arbitration clause valid |
| D | £175k | Medium-High (6/10) | Use as leverage, not primary |

---

### 3. Settlement Negotiation Dynamics (`settlement-negotiation.yml`)

**Purpose:** Model negotiation scenarios and optimal settlement timing

**Triggers:** `settlement`, `negotiation`, `mediation`, `compromise`

**Negotiation Stages:**

**Stage 1: Pre-Filing (Leverage: Plaintiff)**
```
Plaintiff demand: £500k
Defendant offer: £50k (nuisance value)
Zone of possible agreement: £150k-£300k
BATNA (Best Alternative): File lawsuit (£150k cost)
WATNA (Worst Alternative): Lose at trial, get £0
Recommendation: Hold firm, file if no movement
```

**Stage 2: Post-Discovery (Leverage: Shifts based on evidence)**
```
Scenario A (Strong plaintiff evidence):
  Plaintiff demand: £450k (reduced from £500k)
  Defendant offer: £200k (increased from £50k)
  Zone: £300k-£350k
  Recommendation: Settle at £325k

Scenario B (Weak plaintiff evidence):
  Plaintiff demand: £300k (reduced from £500k)
  Defendant offer: £100k (slight increase)
  Zone: £150k-£200k
  Recommendation: Consider £175k or proceed to trial
```

**Stage 3: Pre-Trial (Leverage: Uncertainty favors settlement)**
```
Plaintiff trial risk: 45% chance of losing → £0
Defendant trial risk: 55% chance of £500k verdict = £275k expected value
Both sides face £100k additional trial costs
Zone: £200k-£275k (both better off settling)
Recommended: £237.5k (split the difference)
```

**Mediation Simulation:**
- Neutral mediator shuttles between rooms
- Reality testing ("What if you lose?")
- Non-binding until signed
- Confidential (can't use statements at trial)

**Psychological Factors:**
- Anchoring bias (first number sets range)
- Loss aversion (parties fight harder to avoid loss)
- Sunk cost fallacy ("We've spent £100k, can't settle low")
- Reactive devaluation (reject opponent's offer automatically)

---

### 4. Procedural Default Analysis (`procedural-default.yml`)

**Purpose:** Identify fatal procedural errors that waive substantive rights

**Triggers:** `procedural default`, `waiver`, `deadline missed`, `standing`

**Common Procedural Traps:**

**Trap 1: Statute of Limitations**
```
Claim accrual date: June 1, 2024
Limitation period: 6 years (contract), 3 years (tort)
Filing deadline: June 1, 2030 (contract claim)
Risk: If filed June 2, 2030 → DISMISSED with prejudice
Exception: Minor plaintiff (tolling until age 18)
```

**Trap 2: Failure to Serve**
```
Complaint filed: March 1, 2025
Service deadline: May 1, 2025 (90 days under CPR 7.5)
Actual service: May 15, 2025
Result: DISMISSED without prejudice (refile + re-serve)
Statute barred? Yes → Case dead forever
```

**Trap 3: Lack of Standing**
```
Plaintiff: Assignee of original contracting party
Challenge: Assignment invalid (no consideration)
Ruling: No standing → DISMISSED for lack of jurisdiction
Can cure? Re-file with original party as plaintiff
Time-barred? Yes → Case dead
```

**Trap 4: Arbitration Waiver**
```
Contract has mandatory arbitration clause
Plaintiff files in court
Defendant answers (doesn't move to compel)
Participates in discovery for 6 months
Result: Arbitration right WAIVED (must litigate)
```

**Simulation Output:**
- Procedural checklist (20+ items)
- Critical deadlines (calendar invites set)
- Service proof requirements
- Standing documentation needed
- Risk score per trap (1-10)

---

### 5. Enforcement & Collection (`enforcement-collection.yml`)

**Purpose:** Validate ability to collect judgment after winning

**Triggers:** `enforcement`, `collection`, `judgment recovery`, `asset search`

**Post-Judgment Scenario:**
```
Judgment: £500k + £50k costs + interest (8% per annum)
Defendant status: No liquid assets, business operating
Collection timeline: 6-24 months
Collection cost: 10-30% of recovery
```

**Collection Strategies:**

**Strategy 1: Bank Account Levy**
- Locate accounts via debtor examination
- Sheriff freezes account
- Funds turned over to court
- Yield: £20k-£100k (what's available)
- Time: 2-4 weeks

**Strategy 2: Accounts Receivable Garnishment**
- Court order to defendant's customers
- They pay you instead of defendant
- Yield: £50k-£200k (over 6-12 months)
- Time: Ongoing

**Strategy 3: Property Lien**
- Record judgment lien on real estate
- Blocks sale/refinance until paid
- Yield: £0 until property sells
- Leverage: High (forces negotiation)

**Strategy 4: Corporate Veil Piercing**
- Sue individual shareholders
- Theory: Alter ego / undercapitalization
- Success rate: <10% (very hard)
- Cost: £50k+ additional litigation

**Strategy 5: Contempt Proceedings**
- Defendant hiding assets?
- Court orders asset disclosure
- Refusal = contempt (jail until comply)
- Nuclear option (use sparingly)

**Asset Search Tools:**
- Land registry search (£3-£10 per property)
- Company House filings (UK entities)
- Social media intelligence (lifestyle vs. broke claim)
- Debtor exam (court-ordered questioning)

**Realistic Recovery Scenarios:**
- **Best case (solvent defendant):** 100% collection in 3 months
- **Typical case (struggling business):** 40-60% over 12-18 months
- **Worst case (judgment-proof):** 0-10% over 24+ months

---

## MiroFish Integration

### Auto-Trigger Keywords

| Keyword | Scenario | Priority |
|---------|----------|----------|
| `appeal`, `апелляция` | appeal-dynamics.yml | High |
| `strategy options`, `пересмотр` | case-permutation.yml | Medium |
| `settlement`, `медиация` | settlement-negotiation.yml | High |
| `procedural default`, `waiver` | procedural-default.yml | Critical |
| `enforcement`, `collection` | enforcement-collection.yml | Medium |

### Running Simulations

**Manual trigger:**
```bash
cd ~/ss1
bash ../mirofish-engine/run.sh appeal-dynamics
```

---

## Memory Updates

After each simulation:

```markdown
## 2026-04-03 — Appeal Dynamics Simulation

**Scenario:** appeal-dynamics.yml (summary judgment reversal)  
**Result:** PASSED with timeline validated  
**Key Finding:** 180-day oral argument wait typical  
**Action:** File notice of appeal by Day 30, budget 6 months for decision  
**Owner:** @bereg2022
```

---

**Source:** `~/developer/docs/MIROFISH-SCENARIOS-ss1.md` (MASTER)  
**Synced:** N/A (project-specific)  
**Last Updated:** 2026-04-03
