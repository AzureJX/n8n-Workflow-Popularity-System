from collectors.youtube_collector import collect_youtube
from collectors.discourse_collector import collect_discourse
from collectors.trends_collector import collect_trends
from database import SessionLocal, Workflow
from datetime import datetime

def save_workflows(workflows):
    """Save collected workflows into SQLite DB and return count."""
    db = SessionLocal()
    inserted_count = 0
    try:
        for wf in workflows:
            db_workflow = Workflow(
                workflow=wf["workflow"],
                platform=wf["platform"],
                popularity_metrics=wf["popularity_metrics"],
                country=wf["country"],
                collected_at=datetime.utcnow(),
            )
            db.add(db_workflow)
            inserted_count += 1
        db.commit()
    finally:
        db.close()
    return inserted_count
        
def collect_all():
    workflows = []

    # YouTube
    yt_data = collect_youtube(query="n8n workflow", max_results=20, region="US")
    yt_data += collect_youtube(query="n8n workflow", max_results=20, region="IN")
    workflows.extend(yt_data)

    # Discourse
    workflows.extend(collect_discourse(category_id=19, max_topics=20))

    # Google Trends
    workflows.extend(collect_trends(["n8n workflow", "n8n slack integration"], geo="US"))
    workflows.extend(collect_trends(["n8n workflow", "n8n slack integration"], geo="IN"))

    inserted_count = 0
    if workflows:
        inserted_count = save_workflows(workflows)

    return inserted_count