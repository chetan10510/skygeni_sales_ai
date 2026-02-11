import os
from openai import OpenAI


class AINarrative:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment.")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def generate_summary(self, intent, metrics, risk_summary, health_score):

        formatted_metrics = f"""
WIN RATE: {metrics['overall_win_rate']*100:.2f} percent
WIN RATE TREND: {metrics['win_rate_trend']}
WEAKEST LEAD SOURCE: {metrics['weakest_lead_source']}
AVERAGE SALES CYCLE: {metrics['average_sales_cycle']} days
MEDIAN SALES CYCLE: {metrics['median_sales_cycle']} days
STALLED DEALS: {metrics['stalled_deal_percentage']*100:.2f} percent
MEAN ACV: {metrics['acv_stats']['mean_acv']:.2f}
TOTAL REVENUE: {metrics['acv_stats']['total_revenue']:.2f}
HIGH RISK PERCENTAGE: {risk_summary['high_risk_percentage']*100:.2f}
PIPELINE HEALTH SCORE: {health_score}
"""

        prompt = f"""
You are an executive sales intelligence analyst.

Answer the user's question directly.
If win rate is declining, explain why using trend and weakest segment data.
Identify probable root causes using provided metrics.

Respond ONLY in valid JSON.

Format:

{{
  "executive_summary": "",
  "key_risks": [],
  "data_insights": [],
  "recommended_actions": [],
  "confidence_score": ""
}}

User Intent: {intent}

Metrics:
{formatted_metrics}
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Output clean JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        return content
