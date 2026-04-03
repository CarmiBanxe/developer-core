# docs/MIROFISH-SCENARIOS.md — ГИЙОН Legal Platform

**Project:** guiyon  
**Type:** Legal/Court Strategy  
**MiroFish Role:** Litigation strategy simulation & counter-argument stress-testing  
**Auto-trigger:** Legal keywords (суд, апелляция, контраргумент, иск)

---

## Scenario Library

### 1. Court Strategy Simulation (`court-strategy.yml`)

**Purpose:** Model optimal litigation approach before filing

**Triggers:** `court`, `суд`, `litigation`, `исковое заявление`, `strategy`

**Agents:**
- **Plaintiff Attorney (Вы):** Builds the case
- **Defense Attorney:** Anticipates opponent's arguments
- **Judge (Судья):** Evaluates legal merit, procedural compliance
- **Expert Witness:** Technical/financial specialist
- **Court Clerk:** Procedural requirements checker

**Case Structure:**
```
Claim: Breach of contract + damages (£250k)
Elements:
  1. Contract existence (written? oral? implied?)
  2. Plaintiff performance (did we deliver?)
  3. Defendant breach (what specific terms violated?)
  4. Causation (breach → damages chain)
  5. Damages calculation (how £250k derived?)
```

**Simulation Flow:**
1. **Opening Statement (Plaintiff):** 5-minute pitch
2. **Defense Motion to Dismiss:** "Failure to state a claim"
3. **Judge's Ruling:** Grant/deny with reasoning
4. **Discovery Phase:** Document requests, depositions
5. **Summary Judgment:** "No genuine dispute of material fact"
6. **Trial Preparation:** Witness prep, exhibit lists
7. **Verdict Prediction:** Win probability + damages range

**Validation Metrics:**
- Claim survival rate ( survives motion to dismiss?)
- Evidence strength score (0-10 per element)
- Judge's preliminary leanings (plaintiff/defense/neutral)
- Settlement recommendation (if win prob < 60%)

---

### 2. Judge Reaction Modeling (`judge-reaction.yml`)

**Purpose:** Predict judicial response to specific arguments

**Triggers:** `judge reaction`, `судья реакция`, `judicial bias`, `ruling prediction`

**Judge Profiles Simulated:**

**Judge A (Strict Constructionist):**
- Focus: Text of contract, statute language
- Skepticism: Extrapolated damages, emotional appeals
- Likely questions: "Show me the clause", "Cite the statute"
- Win rate: 52% plaintiff / 48% defense

**Judge B (Equity-Oriented):**
- Focus: Fairness, intent, unconscionability
- Skepticism: Technical loopholes, harsh forfeitures
- Likely questions: "Is this result just?", "What did parties intend?"
- Win rate: 58% plaintiff / 42% defense

**Judge C (Procedural Formalist):**
- Focus: Deadlines, proper service, standing
- Skepticism: Late filings, informal communications
- Likely questions: "Was this filed timely?", "Do you have standing?"
- Win rate: 45% plaintiff / 55% defense (dismissals common)

**Argument Testing:**
```
Argument: "Defendant acted in bad faith"
Judge A: "Define bad faith. Cite precedent." (legal standard)
Judge B: "How did this harm your client?" (equity focus)
Judge C: "Is this pled in Paragraph 12?" (procedural check)
```

**Output:** Argument effectiveness score per judge profile

---

### 3. Appeal Dynamics (`appeal-dynamics.yml`)

**Purpose:** Simulate appellate court review process

**Triggers:** `appeal`, `апелляция`, `reversal`, `appellate brief`

**Appellate Standards of Review:**
- **De novo:** Fresh look at law (no deference to trial court)
- **Abuse of discretion:** Highly deferential (must show arbitrary ruling)
- **Clearly erroneous:** Factual findings (very hard to overturn)
- **Harmless error:** Even if wrong, did it affect outcome?

**Appeal Scenarios:**

**Scenario A: Error of Law**
```
Trial ruling: "Statute of limitations expired"
Standard: De novo review
Strength: Strong (appellate courts decide law independently)
Reversal probability: 45%
```

**Scenario B: Evidentiary Ruling**
```
Trial ruling: "Expert testimony excluded"
Standard: Abuse of discretion
Strength: Weak (trial judge has broad latitude)
Reversal probability: 15%
```

**Scenario C: Damages Award**
```
Trial verdict: £250k compensatory + £1M punitive
Standard: Shock the conscience test
Strength: Moderate (punitive easier to challenge)
Reversal probability: 30% (punitive portion)
```

**Appellate Brief Structure:**
1. **Question Presented:** One sentence framing the issue
2. **Statement of Facts:** Favorable but accurate narrative
3. **Argument:** IRAC format (Issue, Rule, Analysis, Conclusion)
4. **Conclusion:** Specific relief requested (reverse/remand/affirm)

**Oral Argument Simulation:**
- Appellate judge interrupts every 90 seconds
- Questions reveal panel's concerns
- Weaknesses exposed under rapid-fire questioning

---

### 4. Counter-Argument Stress Test (`counter-argument.yml`)

**Purpose:** Identify vulnerabilities in legal reasoning

**Triggers:** `counter-argument`, `контраргумент`, `weakness`, `vulnerability`

**Stress Test Method:**

**Your Argument:**
> "Defendant breached Section 5.2 by failing to deliver goods by June 1. This caused £250k in lost profits."

**Red Team Attacks:**

**Attack 1 (Contract Interpretation):**
> "Section 5.2 says 'best efforts to deliver by June 1' — not absolute guarantee. Defendant made best efforts despite supplier delay."

**Attack 2 (Causation):**
> "Lost profits speculative. Market downturn in Q3 also contributed. Expert didn't isolate breach impact from other factors."

**Attack 3 (Mitigation):**
> "Plaintiff could have purchased substitute goods. Failed to mitigate damages. Reduction: 40%."

**Attack 4 (Liquidated Damages):**
> "Contract Section 12.3 limits remedy to purchase price refund (£50k). Waiver of consequential damages."

**Your Rebuttals Required:**
- Best efforts vs. strict performance (cite precedent)
- Damage model methodology (Daubert challenge prep)
- Mitigation feasibility (evidence needed)
- Liquidated damages enforceability (unconscionability argument)

**Vulnerability Score:** 0-10 per attack vector  
**Recommendation:** Strengthen causation evidence, prepare Daubert motion

---

### 5. Witness Credibility Analysis (`witness-credibility.yml`)

**Purpose:** Evaluate witness reliability under cross-examination

**Triggers:** `witness`, `testimony`, `cross-examination`, `credibility`

**Witness Profiles:**

**Expert Witness (Dr. Smith, Economist):**
- **Direct Examination:** Damages model explained clearly
- **Cross-Examination Vulnerabilities:**
  - Assumptions not peer-reviewed
  - Previously testified for plaintiff 15 times (hired gun?)
  - Data source limitations acknowledged
- **Credibility Score:** 7/10 (qualified but biased)

**Fact Witness (John Doe, CFO):**
- **Direct Examination:** Contract negotiations recounted
- **Cross-Examination Vulnerabilities:**
  - Memory gaps ("I don't recall")
  - Email contradicts testimony
  - Financial interest in outcome
- **Credibility Score:** 5/10 (self-serving)

**Hostile Witness (Jane Roe, Defendant CEO):**
- **Direct Examination:** Minimal cooperation
- **Cross-Examination Opportunities:**
  - Prior inconsistent statement (deposition vs. trial)
  - Admission on key element (breach intentional)
  - Evasive answers damage credibility
- **Credibility Score:** 4/10 (adverse but damaging admissions)

**Cross-Examination Simulation:**
```
Q: "You testified X in deposition, correct?"
A: "Yes."
Q: "Email dated June 15 says Y. Which is true?"
A: "Context matters..."
Q: "Simple yes or no: Is email accurate?"
A: [Commit or evade?]"
```

**Output:** Recommended cross-examination topics (top 3 per witness)

---

## MiroFish Integration

### Auto-Trigger Keywords

| Keyword | Scenario | Priority |
|---------|----------|----------|
| `court`, `суд`, `иск` | court-strategy.yml | High |
| `judge`, `судья`, `ruling` | judge-reaction.yml | Medium |
| `appeal`, `апелляция` | appeal-dynamics.yml | High |
| `counter-argument`, `уязвимость` | counter-argument.yml | Critical |
| `witness`, `testimony` | witness-credibility.yml | Medium |

### Running Simulations

**Manual trigger:**
```bash
cd ~/guiyon
bash ../mirofish-engine/run.sh court-strategy
```

---

## Memory Updates

After each simulation:

```markdown
## 2026-04-03 — Court Strategy Simulation

**Scenario:** court-strategy.yml (breach of contract claim)  
**Result:** PASSED with vulnerabilities identified  
**Key Finding:** Causation element weakest ( Attack 2)  
**Action:** Retain independent economist for Daubert-proof expert report  
**Owner:** @bereg2022
```

---

**Source:** `~/developer/docs/MIROFISH-SCENARIOS-guiyon.md` (MASTER)  
**Synced:** N/A (project-specific)  
**Last Updated:** 2026-04-03
