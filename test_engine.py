#This is a test file to validate the integration of the DecisionEngine, RiskModel, and HealthIndex classes. It loads the sales data, computes the necessary metrics, evaluates the risk, and calculates the health score of the sales pipeline. Finally, it prints out the results for verification.

from decision_engine import DecisionEngine
from risk_model import RiskModel
from health_index import HealthIndex

engine = DecisionEngine("data/skygeni_sales_data.csv")
metrics = engine.compute_all_metrics()

risk_model = RiskModel(engine.df)
risk_summary = risk_model.portfolio_risk_summary()

health_model = HealthIndex(metrics, risk_summary)
health_score = health_model.compute_health_score()
label = health_model.health_label(health_score)

print("Metrics:", metrics)
print("Risk Summary:", risk_summary)
print("Pipeline Health Score:", health_score)
print("Pipeline Status:", label)