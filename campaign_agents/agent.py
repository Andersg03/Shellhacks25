from google.adk.agents import ParallelAgent, SequentialAgent, LoopAgent
from .subagents.pytrends_agent import pytrend_agent
from .subagents.google_search_agent import google_search_agent
from .subagents.reddit_agent import reddit_agent
from .subagents.campaign_creator_agent import campaign_creator_agent

trend_data_collector = ParallelAgent(
    name="trend_data_collector",
    sub_agents=[pytrend_agent,google_search_agent, reddit_agent],
)
root_agent = SequentialAgent(
    name="Control-Agent",
    sub_agents=[trend_data_collector, # Step 1: Collect trend data from google trends, google searches, and reddit
                campaign_creator_agent, # Step 2: Create initial marketing campaign
                #campaign_refiner
                ], # Step 3: Refine marketing campaign within a loop agent until satisfied
)