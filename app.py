from fastapi import FastAPI, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Workflow
from jobs import collect_all
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Initialize database
init_db()

# Run daily
scheduler = BackgroundScheduler()
scheduler.add_job(collect_all, "cron", hour=8, minute=0)
scheduler.start()

templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results")
def results(db: Session = Depends(get_db)):
    """Return stored workflows from SQLite."""
    workflows = db.query(Workflow).all()
    return [
        {
            "workflow": wf.workflow,
            "platform": wf.platform,
            "popularity_metrics": wf.popularity_metrics,
            "country": wf.country,
            "collected_at": wf.collected_at,
        }
        for wf in workflows
    ]

@app.get("/results_page", response_class=HTMLResponse)
def results_page(request: Request, db: Session = Depends(get_db)):
    """Return stored workflows in an HTML page."""
    workflows = db.query(Workflow).all()
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "workflows": workflows}
    )

@app.get("/refresh")
def refresh():
    """Force refresh workflows (manual trigger)."""
    data = collect_all()
    return {"inserted": len(data)}

@app.get("/refresh_page", response_class=HTMLResponse)
def refresh_page(request: Request):
    """Trigger data collection and show how many workflows were added."""
    inserted = collect_all()
    return templates.TemplateResponse(
        "refresh.html",
        {"request": request, "inserted": inserted}
    )