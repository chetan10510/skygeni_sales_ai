import pandas as pd


class RiskModel:
    def __init__(self, df):
        self.df = df.copy()
        self.median_cycle = self.df["sales_cycle_days"].median()
        self.median_acv = self.df["deal_amount"].median()

    # -----------------------------
    # Risk Components
    # -----------------------------

    def cycle_risk(self):
        # Normalize cycle days
        max_cycle = self.df["sales_cycle_days"].max()
        return (self.df["sales_cycle_days"] / max_cycle)

    def acv_risk(self):
        # Lower ACV = higher risk
        return (self.median_acv - self.df["deal_amount"]) / self.median_acv

    def lead_source_risk(self):
        # Assign static risk values (can refine later)
        risk_map = {
            "Inbound": 0.2,
            "Outbound": 0.4,
            "Partner": 0.3,
            "Referral": 0.25
        }
        return self.df["lead_source"].map(risk_map).fillna(0.3)

    def stall_risk(self):
        threshold = 1.5 * self.median_cycle
        return (self.df["sales_cycle_days"] > threshold).astype(int)

    # -----------------------------
    # Final Risk Score
    # -----------------------------

    def compute_risk_score(self):
        self.df["cycle_risk"] = self.cycle_risk()
        self.df["acv_risk"] = self.acv_risk()
        self.df["lead_source_risk"] = self.lead_source_risk()
        self.df["stall_risk"] = self.stall_risk()

        # Weighted risk score
        self.df["risk_score"] = (
            0.35 * self.df["cycle_risk"] +
            0.25 * self.df["acv_risk"] +
            0.20 * self.df["lead_source_risk"] +
            0.20 * self.df["stall_risk"]
        )

        # Scale to 0–100
        self.df["risk_score"] = (self.df["risk_score"] * 100).clip(0, 100)

        return self.df

    # -----------------------------
    # Portfolio Risk Summary
    # -----------------------------

    def portfolio_risk_summary(self):
        df = self.compute_risk_score()

        high_risk = df[df["risk_score"] > 60]
        medium_risk = df[(df["risk_score"] > 30) & (df["risk_score"] <= 60)]
        low_risk = df[df["risk_score"] <= 30]

        return {
            "average_risk_score": round(df["risk_score"].mean(), 2),
            "high_risk_percentage": round(len(high_risk) / len(df), 4),
            "medium_risk_percentage": round(len(medium_risk) / len(df), 4),
            "low_risk_percentage": round(len(low_risk) / len(df), 4)
        }
