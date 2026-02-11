import pandas as pd


class DecisionEngine:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_data()
        self.clean_data()

    def load_data(self):
        return pd.read_csv(self.file_path)

    def clean_data(self):
        self.df["created_date"] = pd.to_datetime(self.df["created_date"], errors="coerce")
        self.df["closed_date"] = pd.to_datetime(self.df["closed_date"], errors="coerce")
        self.df["outcome"] = self.df["outcome"].str.lower().str.strip()
        self.df = self.df.dropna(subset=["deal_amount", "sales_cycle_days"])

    # -----------------------------
    # Core Metrics
    # -----------------------------

    def overall_win_rate(self):
        closed = self.df[self.df["outcome"].isin(["won", "lost"])]
        if len(closed) == 0:
            return 0
        return round((closed["outcome"] == "won").mean(), 4)

    def win_rate_by_lead_source(self):
        closed = self.df[self.df["outcome"].isin(["won", "lost"])]
        grouped = closed.groupby("lead_source")["outcome"].apply(
            lambda x: (x == "won").mean()
        )
        return grouped.round(4).to_dict()

    def weakest_lead_source(self):
        closed = self.df[self.df["outcome"].isin(["won", "lost"])]
        grouped = closed.groupby("lead_source")["outcome"].apply(
            lambda x: (x == "won").mean()
        )
        weakest = grouped.idxmin()
        return {
            "weakest_source": weakest,
            "win_rate": round(grouped.min(), 4)
        }

    def win_rate_trend(self):
        df = self.df[self.df["outcome"].isin(["won", "lost"])].copy()
        df["year_quarter"] = df["created_date"].dt.to_period("Q")

        quarterly_win = df.groupby("year_quarter")["outcome"].apply(
            lambda x: (x == "won").mean()
        )

        if len(quarterly_win) < 2:
            return {"trend_direction": "Insufficient data"}

        trend_value = quarterly_win.diff().mean()

        if trend_value < 0:
            direction = "Declining"
        elif trend_value > 0:
            direction = "Improving"
        else:
            direction = "Stable"

        return {
            "trend_direction": direction,
            "latest_win_rate": round(quarterly_win.iloc[-1], 4),
            "previous_win_rate": round(quarterly_win.iloc[-2], 4)
        }

    def average_sales_cycle(self):
        return round(self.df["sales_cycle_days"].mean(), 2)

    def median_sales_cycle(self):
        return round(self.df["sales_cycle_days"].median(), 2)

    def stalled_deal_percentage(self):
        median_cycle = self.median_sales_cycle()
        threshold = 1.5 * median_cycle
        stalled = self.df[self.df["sales_cycle_days"] > threshold]
        return round(len(stalled) / len(self.df), 4)

    def acv_stats(self):
        return {
            "mean_acv": round(self.df["deal_amount"].mean(), 2),
            "median_acv": round(self.df["deal_amount"].median(), 2),
            "total_revenue": round(self.df["deal_amount"].sum(), 2)
        }

    # -----------------------------
    # Master Metric Function
    # -----------------------------

    def compute_all_metrics(self):
        return {
            "overall_win_rate": self.overall_win_rate(),
            "win_rate_by_lead_source": self.win_rate_by_lead_source(),
            "weakest_lead_source": self.weakest_lead_source(),
            "win_rate_trend": self.win_rate_trend(),
            "average_sales_cycle": self.average_sales_cycle(),
            "median_sales_cycle": self.median_sales_cycle(),
            "stalled_deal_percentage": self.stalled_deal_percentage(),
            "acv_stats": self.acv_stats(),
            "total_deals": len(self.df)
        }
