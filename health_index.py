class HealthIndex:
    def __init__(self, metrics, risk_summary):
        self.metrics = metrics
        self.risk_summary = risk_summary

    def compute_health_score(self):
        win_rate_strength = self.metrics["overall_win_rate"] * 100
        low_risk_strength = (1 - self.risk_summary["high_risk_percentage"]) * 100

        avg_cycle = self.metrics["average_sales_cycle"]
        median_cycle = self.metrics["median_sales_cycle"]

        # Normalize velocity (lower cycle = better)
        velocity_strength = max(0, 100 - ((avg_cycle / (median_cycle * 2)) * 100))

        low_stall_strength = (1 - self.metrics["stalled_deal_percentage"]) * 100

        health_score = (
            0.40 * win_rate_strength +
            0.30 * low_risk_strength +
            0.20 * velocity_strength +
            0.10 * low_stall_strength
        )

        return round(health_score, 2)

    def health_label(self, score):
        if score >= 75:
            return "Strong Pipeline"
        elif score >= 55:
            return "Moderate Pipeline"
        else:
            return "At Risk"
