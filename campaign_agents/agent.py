from google.adk.agents import ParallelAgent, SequentialAgent, LoopAgent
from subagents.pytrends_agent import pytrend_agent

trend_data_collector = ParallelAgent(
    name="trend_data_collector",
    sub_agents=[pytrend_agent,],
)

campaign_refiner = LoopAgent(
    name="campaign_refiner",
)

root_agent = SequentialAgent(
    name="Control-Agent",
    sub_agents=[trend_data_collector, campaign_refiner],
)