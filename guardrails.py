class Guardrails:
    def __init__(self):
        self.intent_map = {
            "win_rate": ["win rate", "conversion", "close rate"],
            "risk": [
                "risk",
                "high risk",
                "exposure",
                "likely to be lost",
                "most likely to be lost",
                "probability of loss"
            ],
            "stalled": [
                "stall",
                "stalled",
                "stalling",
                "delay",
                "slow",
                "sales cycle",
                "cycle length",
                "increasing cycle"
            ],
            "acv": ["acv", "deal value", "contract value", "amount"],
            "lead_source": ["lead source", "source performance"],
            "pipeline_health": [
                "pipeline health",
                "overall performance",
                "revenue outcomes",
                "improve revenue",
                "revenue improvement",
                "actions improve revenue"
            ]
        }

    def detect_intent(self, query):
        query = query.lower()

        for intent, keywords in self.intent_map.items():
            for word in keywords:
                if word in query:
                    return intent

        return None
