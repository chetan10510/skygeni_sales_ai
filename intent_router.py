from visualizations import (
    win_rate_by_source_chart,
    risk_distribution_chart,
    acv_distribution_chart,
    acv_vs_risk_scatter,
    sales_cycle_distribution,
    health_score_gauge,
    win_rate_trend_chart
)


def route_visuals(intent, metrics, df, risk_df, health_score):
    visuals = []

    if intent == "win_rate":
        visuals.append(win_rate_trend_chart(df))
        visuals.append(win_rate_by_source_chart(metrics["win_rate_by_lead_source"]))

    elif intent == "risk":
        visuals.append(risk_distribution_chart(risk_df))

    elif intent == "acv":
        visuals.append(acv_distribution_chart(risk_df))
        visuals.append(acv_vs_risk_scatter(risk_df))

    elif intent == "stalled":
        visuals.append(sales_cycle_distribution(df))

    elif intent == "pipeline_health":
        visuals.append(health_score_gauge(health_score))
        visuals.append(risk_distribution_chart(risk_df))

    return visuals
