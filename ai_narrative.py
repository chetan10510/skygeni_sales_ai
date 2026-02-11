import os
from openai import OpenAI


class AINarrative:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if api_key:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        else:
            self.client = None

    def generate_summary(self, user_query, intent, metrics, risk_summary, health_score):

        # -----------------------------
        # Deterministic Executive Logic
        # -----------------------------

        if intent == "risk":
            return {
                "executive_summary": (
                    f"{risk_summary['high_risk_percentage']*100:.2f}% of deals fall into the high-risk category "
                    f"with an average risk score of {risk_summary['average_risk_score']}. "
                    "These deals are most likely to be lost, particularly those exceeding the median sales cycle."
                ),
                "key_risks": [
                    f"High-risk exposure: {risk_summary['high_risk_percentage']*100:.2f}%",
                    f"Average risk score: {risk_summary['average_risk_score']}",
                    f"Stalled deals: {metrics['stalled_deal_percentage']*100:.2f}%"
                ],
                "data_insights": [
                    f"High Risk Percentage: {risk_summary['high_risk_percentage']*100:.2f}%",
                    f"Average Risk Score: {risk_summary['average_risk_score']}"
                ],
                "recommended_actions": [
                    "Prioritize intervention on high-risk, high-ACV deals.",
                    "Escalate stalled opportunities exceeding cycle thresholds.",
                    "Review lead source quality contributing to risk exposure."
                ],
                "confidence_score": "High"
            }

        if intent == "win_rate":
            trend = metrics["win_rate_trend"]
            weakest = metrics["weakest_lead_source"]

            return {
                "executive_summary": (
                    f"Win rate is {trend['trend_direction'].lower()}, moving from "
                    f"{trend.get('previous_win_rate', 0)*100:.2f}% to "
                    f"{trend.get('latest_win_rate', 0)*100:.2f}%. "
                    f"The weakest lead source is {weakest['weakest_source']} "
                    f"with a win rate of {weakest['win_rate']*100:.2f}%."
                ),
                "key_risks": [
                    f"Declining win-rate trend: {trend['trend_direction']}",
                    f"Weakest lead source: {weakest['weakest_source']}"
                ],
                "data_insights": [
                    f"Previous Win Rate: {trend.get('previous_win_rate', 0)*100:.2f}%",
                    f"Latest Win Rate: {trend.get('latest_win_rate', 0)*100:.2f}%"
                ],
                "recommended_actions": [
                    "Rebalance acquisition mix toward higher-performing lead sources.",
                    "Investigate stalled deals contributing to conversion pressure.",
                    "Audit qualification standards for weaker segments."
                ],
                "confidence_score": "High"
            }

        if intent == "pipeline_health":
            return {
                "executive_summary": (
                    f"Pipeline health score is {health_score}, reflecting current conversion efficiency, "
                    f"risk exposure of {risk_summary['high_risk_percentage']*100:.2f}%, "
                    f"and stalled deal ratio of {metrics['stalled_deal_percentage']*100:.2f}%."
                ),
                "key_risks": [
                    f"High-risk exposure: {risk_summary['high_risk_percentage']*100:.2f}%",
                    f"Stalled deals: {metrics['stalled_deal_percentage']*100:.2f}%"
                ],
                "data_insights": [
                    f"Pipeline Health Score: {health_score}",
                    f"Win Rate Trend: {metrics['win_rate_trend']['trend_direction']}"
                ],
                "recommended_actions": [
                    "Reduce stalled deal backlog.",
                    "Mitigate high-risk revenue concentration.",
                    "Improve lead source performance variance."
                ],
                "confidence_score": "High"
            }

        if intent == "stalled":
            return {
                "executive_summary": (
                    f"{metrics['stalled_deal_percentage']*100:.2f}% of deals exceed 1.5× median sales cycle, "
                    "indicating potential bottlenecks in deal progression."
                ),
                "key_risks": [
                    f"Elevated stalled deal ratio: {metrics['stalled_deal_percentage']*100:.2f}%"
                ],
                "data_insights": [
                    f"Median Sales Cycle: {metrics['median_sales_cycle']} days"
                ],
                "recommended_actions": [
                    "Audit delayed opportunities.",
                    "Introduce cycle acceleration initiatives.",
                    "Reprioritize long-running deals."
                ],
                "confidence_score": "High"
            }

        # -----------------------------
        # Fallback to LLM if needed
        # -----------------------------

        if self.client:
            prompt = f"""
Answer the following executive sales question clearly and concisely:

"{user_query}"

Use only these metrics:
{metrics}
{risk_summary}
Health Score: {health_score}

Return JSON:
{{
  "executive_summary": "",
  "key_risks": [],
  "data_insights": [],
  "recommended_actions": [],
  "confidence_score": ""
}}
"""

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            content = response.choices[0].message.content.strip()

            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()

            import json
            return json.loads(content)

        # Absolute fallback
        return {
            "executive_summary": "Deterministic analysis completed.",
            "key_risks": [],
            "data_insights": [],
            "recommended_actions": [],
            "confidence_score": "Moderate"
        }
