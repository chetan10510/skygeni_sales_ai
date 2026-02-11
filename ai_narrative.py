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

    def generate_summary(self, user_query, intent, metrics, risk_summary, health_score):

        formatted_metrics = f"""
OVERALL WIN RATE: {metrics['overall_win_rate']*100:.2f}%
WIN RATE TREND: {metrics['win_rate_trend']}
WEAKEST LEAD SOURCE: {metrics['weakest_lead_source']}
AVERAGE SALES CYCLE: {metrics['average_sales_cycle']} days
MEDIAN SALES CYCLE: {metrics['median_sales_cycle']} days
STALLED DEALS: {metrics['stalled_deal_percentage']*100:.2f}%
MEAN ACV: {metrics['acv_stats']['mean_acv']:.2f}
TOTAL REVENUE: {metrics['acv_stats']['total_revenue']:.2f}
HIGH RISK PERCENTAGE: {risk_summary['high_risk_percentage']*100:.2f}%
AVERAGE RISK SCORE: {risk_summary['average_risk_score']}
PIPELINE HEALTH SCORE: {health_score}
"""

        prompt = f"""
You are an executive sales intelligence analyst.

User Question:
"{user_query}"

Primary Intent: {intent}

You MUST answer the user's question directly.

If the question is about:
- Risk → Focus on high-risk deals and loss probability.
- Pipeline health → Focus on overall health score and structural risks.
- Win rate → Use trend and weakest segment.
- Sales cycle → Focus on cycle metrics and stalled deals.
- ACV → Focus on revenue and deal value insights.

Do NOT default to global win-rate commentary unless relevant to the question.

Use only the metrics provided below.
Respond ONLY in valid JSON.

Format strictly:

{{
  "executive_summary": "",
  "key_risks": [],
  "data_insights": [],
  "recommended_actions": [],
  "confidence_score": ""
}}

Metrics:
{formatted_metrics}
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return clean JSON only. No explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        return content
