from google.adk.agents import Agent

campaign_creator_agent = Agent(
    name="campaign_creator_agent",
    description="Synthesizes all data related to our product and the desired audeince into a marketing campaign based on insights from trend data and refined strategies.",
    model="gemini-2.0-flash",
    instructions="""
    Your task is to create a comprehensive marketing campaign based on the insights gathered from trend data
    Pytrends data: 'pytrends_insights'
    Google Search data: 'google_search_insights'
    Reddit data: 'reddit_insights'

    format your response as a detailed marketing campaign plan that includes:
    - Target Audience: Define the specific demographics and psychographics of the audience.
    - Key Messages: Craft compelling messages that resonate with the target audience.
    - Channels: Identify the most effective marketing channels to reach the audience.
    - Tactics: Outline specific tactics and activities to implement the campaign.
    - Timeline: Provide a timeline for the campaign rollout.
    - Metrics: Suggest key performance indicators (KPIs) to measure the success of the campaign

    Please ensure the campaign is data-driven, leveraging the insights from the trend data to inform each aspect of the plan.
    """,
)