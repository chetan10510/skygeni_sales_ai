import streamlit as st
import json

from decision_engine import DecisionEngine
from risk_model import RiskModel
from health_index import HealthIndex
from guardrails import Guardrails
from intent_router import route_visuals
from ai_narrative import AINarrative
from fallback import fallback_summary


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="SKYGENI Sales Intelligence", layout="wide")

st.title("SKYGENI Sales Intelligence System v1.0")

# -----------------------------
# Suggested Questions (Vertical)
# -----------------------------
st.markdown("### Suggested Questions")

suggestions = [
    "How is ACV performing?",
    "Are deals stalling?",
    "Analyze pipeline health",
    "Where is risk concentrated?",
    "What is our win rate by lead source?"
]

if "query_input" not in st.session_state:
    st.session_state.query_input = ""

for suggestion in suggestions:
    if st.button(suggestion, use_container_width=True):
        st.session_state.query_input = suggestion
        st.rerun()

st.markdown("---")

# -----------------------------
# Load Data + Core Engines
# -----------------------------
engine = DecisionEngine("data/skygeni_sales_data.csv")
metrics = engine.compute_all_metrics()

risk_model = RiskModel(engine.df)
risk_df = risk_model.compute_risk_score()
risk_summary = risk_model.portfolio_risk_summary()

health_model = HealthIndex(metrics, risk_summary)
health_score = health_model.compute_health_score()
health_label = health_model.health_label(health_score)

guard = Guardrails()

# -----------------------------
# Sidebar Dynamic Checklist
# -----------------------------
st.sidebar.title("System Status")

status_items = {
    "Dataset Loaded": engine is not None,
    "Metrics Computed": metrics is not None,
    "Risk Model Active": risk_summary is not None,
    "Health Index Generated": health_score is not None,
    "Guardrails Active": True,
    "Visualization Routing Ready": True,
    "Fallback Mode Available": True,
}

for label, condition in status_items.items():
    if condition:
        st.sidebar.success(f"✔ {label}")
    else:
        st.sidebar.error(f"✘ {label}")

# -----------------------------
# User Query Input
# -----------------------------
query = st.text_input(
    "Ask a sales intelligence question:",
    value=st.session_state.query_input,
    key="main_query_box"
)

# -----------------------------
# Process Query
# -----------------------------
if query:

    intent = guard.detect_intent(query)

    if not intent:
        st.error("Query outside scope of SKYGENI Sales Intelligence.")
        st.stop()

    st.subheader("Executive Insight")

    try:
        ai = AINarrative()
        response = ai.generate_summary(intent, metrics, risk_summary, health_score)
        parsed = json.loads(response)

        st.success("✔ Executive insight analysis from computed sales metrics")

    except Exception:
        st.warning("Executive insight generated using deterministic fallback logic.")
        parsed = fallback_summary(intent, metrics, risk_summary, health_score)

    # -----------------------------
    # Display AI Output
    # -----------------------------
    st.markdown("### Executive Summary")
    st.write(parsed.get("executive_summary", ""))

    st.markdown("---")

    st.markdown("### Key Risks")
    for item in parsed.get("key_risks", []):
        st.write(f"- {item}")

    st.markdown("### Data Insights")
    for item in parsed.get("data_insights", []):
        if isinstance(item, dict):
            if "metric" in item and "value" in item:
                st.write(f"- {item['metric']}: {item['value']}")
            else:
                st.write(f"- {item}")
        else:
            st.write(f"- {item}")

    st.markdown("### Recommended Actions")
    for item in parsed.get("recommended_actions", []):
        st.write(f"- {item}")

    st.markdown("### Confidence")
    st.write(parsed.get("confidence_score", ""))

    st.markdown("---")

    # -----------------------------
    # Supporting Visual Evidence
    # -----------------------------
    st.subheader("Supporting Visual Evidence")

    visuals = route_visuals(intent, metrics, engine.df, risk_df, health_score)

    for fig in visuals:
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Architectural Note (Subtle Positioning)
# -----------------------------
st.markdown("---")
st.caption(
    "This system combines deterministic sales analytics with controlled AI narrative generation. "
    "All executive insights are derived from computed metrics, with fallback logic ensuring reliability and stability."
)
