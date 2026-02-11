# SKYGENI Sales Intelligence Platform

## Overview

This project implements a deterministic Sales Intelligence & Decision Engine designed to diagnose declining win rates despite stable pipeline volume.

[User Query]
→
[Streamlit UI Layer]
→
[Guardrails + Intent Detection]
→
[Deterministic Decision Engine]
→
[Risk Model + Health Index]
→
[Visualization Router]
→
[AI Narrative Layer]
→
[Fallback Logic]
→
[Executive Output + Charts]


Instead of building a simple dashboard or chatbot over data, this system separates:

1. **Deterministic analytical computation**
2. **Explainable risk-based decision modeling**
3. **Controlled AI narrative generation (interpretation layer only)**

All insights are grounded in computed metrics. The AI component is used strictly for executive-level narrative generation and does not perform analytical reasoning.

This ensures:

* Interpretability
* Reliability
* Reproducibility
* Executive trust

---

# Part 1 – Problem Framing

## 1. What is the real business problem?

The CRO reports declining win rates while pipeline volume remains stable.

The real issue is not simply “win rate decline.”
It is **conversion efficiency degradation masked by volume stability.**

This suggests potential underlying issues such as:

* Pipeline quality degradation
* Increasing stalled deals
* Lead source mix shift
* Revenue concentration in high-risk segments
* Elongating sales cycles

The objective is to diagnose **why conversion performance is weakening** and identify actionable levers to improve outcomes.

---

## 2. Key Questions the System Must Answer

The system is designed to answer:

* Is win rate declining over time?
* Which segments are underperforming?
* Is the sales cycle length increasing?
* Are deals stalling beyond expected thresholds?
* Which deals are most likely to be lost?
* Where is revenue at risk?
* What actions would most improve revenue outcomes?

---

## 3. Metrics That Matter Most

The system computes:

* Overall Win Rate
* Quarterly Win Rate Trend
* Win Rate by Lead Source
* Weakest Lead Source Identification
* Average & Median Sales Cycle
* Stalled Deal Percentage
* Deal Risk Score (custom metric)
* Pipeline Health Index (custom metric)
* Revenue Concentration
* Portfolio Risk Exposure

---

## 4. Assumptions

* Closed deals represent valid historical performance.
* Sales cycle deviation correlates with risk.
* Lead source impacts conversion probability.
* Heuristic weighting is sufficient for executive diagnostics.
* No external seasonality effects modeled.
* No rep-level normalization performed.

---

# Part 2 – Data Exploration & Business Insights

## Insight 1 – Win Rate Trend Decline

Quarterly trend analysis shows directional movement in win rate over time.

If the trend is declining, this confirms structural performance pressure rather than random fluctuation.

Why it matters:
Sustained decline indicates systemic pipeline quality degradation.

Action:
Investigate segment-level drivers contributing to conversion decline.

---

## Insight 2 – Lead Source Underperformance

The system identifies the weakest-performing lead source and compares it to overall win rate.

Why it matters:
If pipeline mix shifts toward lower-performing sources, overall conversion will drop even if volume remains stable.

Action:
Reallocate acquisition investment toward higher-performing lead sources.

---

## Insight 3 – Elevated Stalled Deal Ratio

Deals exceeding 1.5× median cycle are classified as stalled.

Why it matters:
High stalled ratio reduces velocity and conversion efficiency.

Action:
Escalate long-cycle high-ACV deals for intervention.

---

## Custom Metric 1 – Deal Risk Score (0–100)

Weighted heuristic model combining:

* Cycle deviation risk
* ACV risk
* Lead source baseline risk
* Stall risk

This produces explainable risk scoring per deal.

Purpose:
Identify deals most likely to be lost.

---

## Custom Metric 2 – Pipeline Health Index (0–100)

Composite KPI combining:

* Win rate strength
* Risk exposure
* Stalled ratio
* Velocity indicators

Purpose:
Provide CRO-level quick assessment of overall pipeline condition.

---

# Root Cause Hypothesis

The win-rate decline appears structural rather than random, as trend analysis shows directional movement across consecutive quarters.
Preliminary analysis suggests that win rate pressure may stem from:

* Increasing stalled deal ratio
* Underperformance of specific lead sources
* Elevated revenue concentration in higher-risk deals

This indicates **pipeline mix degradation rather than volume decline**.

Further cohort-level decomposition would strengthen causal validation.

---

# Part 3 – Decision Engine

## Chosen Option: Deal Risk Scoring

The system scores deals most likely to be lost using deterministic logic.

### Risk Model Structure

Risk Score =

* 35% Sales Cycle Deviation
* 25% ACV Risk
* 20% Lead Source Risk
* 20% Stall Classification

Scores normalized 0–100.

---

## Why Heuristic Instead of ML?

* Limited labeled training data
* Executive need for interpretability
* Faster implementation
* Avoid overfitting
* Clear explainability

This prioritizes business usability over predictive complexity.

---

## Actionable Outputs

* High-risk deal identification
* Revenue-at-risk percentage
* Weakest segment identification
* Stalled deal clusters
* Pipeline health status

---

# Part 4 – Mini System Design

## Architecture

User Query
→ Guardrails & Intent Detection
→ Deterministic Decision Engine
→ Risk Model
→ Pipeline Health Index
→ Visualization Router
→ AI Narrative Layer (Interpretation Only)
→ Fallback Logic

---

## Key Design Principle

**Analytics First. AI Second.**

The AI layer:

* Does not compute metrics
* Only interprets structured results
* Is fully optional (fallback logic available)

This prevents hallucinated insights and ensures analytical correctness.

---

## Data Flow

1. Load dataset (5000 rows)
2. Compute deterministic metrics
3. Apply risk scoring
4. Detect intent from user query
5. Route relevant visualizations
6. Generate executive summary
7. Use fallback logic if LLM unavailable

---

## Example Alerts

* “Win rate trend is declining quarter-over-quarter.”
* “High-risk exposure exceeds threshold.”
* “Stalled deals exceed historical median ratio.”
* “Lead source underperformance detected.”

---

## Execution Frequency

* Daily metric recomputation
* Weekly executive summary
* On-demand query analysis

---

## Failure Cases & Limitations

* Static risk weights
* No statistical significance testing
* No cohort-based analysis
* No rep-level normalization
* No seasonality adjustment
* Free-tier inference reliability limitations
* No probabilistic outcome modeling

---

# Part 5 – Reflection

## Weakest Assumptions

* Manual risk weight calibration
* Lead source baseline stability assumption
* No longitudinal customer cohort tracking

---

## What Would Break in Production?

* Data schema changes
* Stage definition inconsistencies
* Scaling beyond in-memory processing
* LLM response structure drift

---

## What I Would Build Next (1 Month Roadmap)

* Cohort-based win-rate shift analysis
* Rep-level normalization modeling
* Logistic regression calibration of risk weights
* Alert automation (Slack/Email)
* Caching layer for large-scale data
* Statistical confidence intervals for trend detection

---

## Least Confident Area

* Heuristic risk weight calibration
* Lack of true probabilistic modeling
* Absence of significance testing on trend changes

---

# How to Run Locally

```bash
git clone <repository_url>
cd skygeni-sales-intelligence
pip install -r requirements.txt
setx GROQ_API_KEY "your_key_here"
streamlit run app.py
```

---

# Deployment

Deployed using:

* Streamlit Community Cloud
* Groq LLM via OpenAI-compatible API
* Fully free-tier compatible

Secrets configured via:

```
GROQ_API_KEY = "<your_groq_api_key>"
```

---

# Key Engineering Decisions

* Deterministic analytics layer separated from AI layer
* Intent-based visualization routing
* Guardrails to prevent scope drift
* Structured JSON enforcement for AI responses
* Fallback narrative logic
* Modular file architecture
* Trend detection integrated into metrics

---

# Why This Approach?

Modern AI systems in business contexts must be:

* Interpretable
* Reliable
* Action-oriented
* Fail-safe

This implementation prioritizes executive trust over model complexity.

---

# Conclusion

This solution is designed not as a notebook analysis, but as a scalable Sales Intelligence prototype that balances:

* Business reasoning
* Engineering structure
* Risk-based modeling
* Controlled AI integration After Computed Analysis
* Production awareness

It provides both diagnostic clarity and actionable guidance for sales leadership.

---

# Final Notes

This system intentionally demonstrates:

* Structured analytical reasoning
* Explainable decision modeling
* Controlled AI usage
* Production-conscious design
* Business-first thinking


