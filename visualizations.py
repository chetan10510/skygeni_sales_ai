import plotly.express as px
import plotly.graph_objects as go


def win_rate_by_source_chart(win_rate_dict):
    sources = list(win_rate_dict.keys())
    values = [v * 100 for v in win_rate_dict.values()]

    fig = px.bar(
        x=sources,
        y=values,
        labels={"x": "Lead Source", "y": "Win Rate (%)"},
        title="Win Rate by Lead Source"
    )

    return fig


def risk_distribution_chart(df):
    fig = px.histogram(
        df,
        x="risk_score",
        nbins=30,
        title="Risk Score Distribution",
        labels={"risk_score": "Risk Score (0–100)"}
    )
    return fig


def acv_distribution_chart(df):
    fig = px.histogram(
        df,
        x="deal_amount",
        nbins=30,
        title="Deal Amount Distribution (ACV)",
        labels={"deal_amount": "Deal Amount"}
    )
    return fig


def acv_vs_risk_scatter(df):
    fig = px.scatter(
        df,
        x="deal_amount",
        y="risk_score",
        title="ACV vs Risk Score",
        labels={"deal_amount": "Deal Amount", "risk_score": "Risk Score"}
    )
    return fig


def sales_cycle_distribution(df):
    fig = px.histogram(
        df,
        x="sales_cycle_days",
        nbins=30,
        title="Sales Cycle Distribution",
        labels={"sales_cycle_days": "Sales Cycle (Days)"}
    )
    return fig


def health_score_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Pipeline Health Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 55], "color": "red"},
                {"range": [55, 75], "color": "orange"},
                {"range": [75, 100], "color": "green"},
            ],
        }
    ))
def win_rate_trend_chart(df):
    closed = df[df["outcome"].isin(["won", "lost"])].copy()
    closed["year_quarter"] = closed["created_date"].dt.to_period("Q")

    trend = closed.groupby("year_quarter")["outcome"].apply(
        lambda x: (x == "won").mean()
    )

    trend = trend.reset_index()
    trend["year_quarter"] = trend["year_quarter"].astype(str)

    fig = px.line(
        trend,
        x="year_quarter",
        y="outcome",
        title="Quarterly Win Rate Trend",
        labels={"outcome": "Win Rate"}
    )
    return fig
