from pytrends.request import TrendReq
from datetime import datetime
import json

def collect_trends(keywords=["n8n workflow"], geo="US"):
    """
    Collects Google Trends data for given keywords and country.
    
    Args:
        keywords (list[str]): Search terms to check.
        geo (str): Country code (US, IN, etc.).
    
    Returns:
        list[dict]: Popularity data.
    """
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(keywords, timeframe="today 3-m", geo=geo)

    # Interest over time
    data = pytrends.interest_over_time()

    results = []
    if not data.empty:
        for keyword in keywords:
            trend_points = data[keyword].tolist()
            avg_interest = sum(trend_points) / len(trend_points)
            results.append({
                "workflow": keyword,
                "platform": "GoogleTrends",
                "popularity_metrics": {
                    "avg_interest": avg_interest,
                    "last_value": trend_points[-1],
                    "trend_points": trend_points[-10:]  # keep last 10 points
                },
                "country": geo,
                "collected_at": datetime.utcnow().isoformat()
            })

    return results

if __name__ == "__main__":
    print(json.dumps(collect_trends(["n8n workflow", "n8n slack integration"], geo="US"), indent=2))