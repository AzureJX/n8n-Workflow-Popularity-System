import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = "AIzaSyCZ0W6EdPeJxcJmaX6Crb3Y6d3cN_buWeg"

BASE_URL = "https://www.googleapis.com/youtube/v3/search"

def collect_youtube(query="n8n workflow", max_results=10, region="US"):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "regionCode": region,
        "key": API_KEY,
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    videos = resp.json().get("items", [])
    
    results = []
    for v in videos:
        vid = v["id"]["videoId"]
        stats = get_video_stats(vid)
        results.append({
            "workflow": v["snippet"]["title"],
            "platform": "YouTube",
            "popularity_metrics": stats,
            "country": region
        })
    return results

def get_video_stats(video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "statistics",
        "id": video_id,
        "key": API_KEY,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    stats = resp.json()["items"][0]["statistics"]
    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))
    return {
        "views": views,
        "likes": likes,
        "comments": comments,
        "like_to_view_ratio": likes / views if views > 0 else 0,
        "comment_to_view_ratio": comments / views if views > 0 else 0,
    }