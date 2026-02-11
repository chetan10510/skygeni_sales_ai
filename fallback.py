def fallback_summary(intent, metrics, risk_summary, health_score):
    return {
        "executive_summary": f"Analysis based on deterministic metrics indicates key performance factors affecting {intent}.",
        "key_risks": [
            f"High risk exposure: {risk_summary['high_risk_percentage']*100:.2f}%",
            f"Stalled deals: {metrics['stalled_deal_percentage']*100:.2f}%"
        ],
        "data_insights": [
            f"Overall win rate: {metrics['overall_win_rate']*100:.2f}%",
            f"Average sales cycle: {metrics['average_sales_cycle']} days"
        ],
        "recommended_actions": [
            "Review high-risk deals exceeding cycle thresholds.",
            "Rebalance pipeline toward higher-performing lead sources.",
            "Increase oversight on stalled opportunities."
        ],
        "confidence_score": "Moderate confidence based on available data."
    }
