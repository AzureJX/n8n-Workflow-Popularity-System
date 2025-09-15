import requests
from datetime import datetime
import json

BASE_URL = "https://community.n8n.io"

def collect_discourse(category_id=19, max_topics=10):
    """
    Collects workflow popularity from the n8n Discourse forum.

    Args:
        category_id (int): Forum category ID (19 = Workflows).
        max_topics (int): Limit on number of topics.

    Returns:
        list[dict]: Forum workflow data.
    """
    url = f"{BASE_URL}/c/{category_id}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for topic in data.get("topic_list", {}).get("topics", [])[:max_topics]:
        results.append({
            "workflow": topic.get("title"),
            "platform": "Discourse",
            "popularity_metrics": {
                "views": topic.get("views"),
                "like_count": topic.get("like_count"),
                "reply_count": topic.get("reply_count"),
                "posters": len(topic.get("posters", []))
            },
            "country": "GLOBAL",
            "collected_at": datetime.utcnow().isoformat()
        })

    return results


if __name__ == "__main__":
    print(json.dumps(collect_discourse(category_id=19, max_topics=10), indent=2))