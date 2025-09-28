from google.adk.agents import Agent
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

def get_pytrends_data(product, audience):
    keywords = [product, audience]
    pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='', gprop='')
    interest = pytrends.interest_over_time()
    related_queries = pytrends.related_queries()
    trending_searches = pytrends.trending_searches()
    return {
        "interest_over_time": interest,
        "related_queries": related_queries,
        "trending_searches": trending_searches
    }

pytrend_agent = Agent(
    name="pytrend_agent",
    model="gemini-2.0-flash",
    description="",
    instructions="""
    You are a helpful ad campaign researcher when the user gives you their product and/ or audience, 
    please use the tool [get_pytrends_data] for pages related to our product and its relation with the desire audience
    factors to consider:
    - interest over time for the product and audience
    - related queries for the product and audience
    - trending searches that might relate to the product and audience
    Use the insights from the get_pytrends_data tool and return a summary of key findings that can help
    """,
    tools=[get_pytrends_data],
    output_key="pytrends_insights"
)