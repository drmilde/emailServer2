# Set up the scheduler
from contextlib import asynccontextmanager

from fastapi import FastAPI
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.interval import IntervalTrigger  # <-- CHANGED IMPORT

# The task to run
def my_daily_task():
    print(f"Task is running at {datetime.now()}")
    # ... additional task code goes here ...

# Set up the scheduler
scheduler = BackgroundScheduler()
trigger = IntervalTrigger(seconds=10)  # <-- CHANGED LINE (run every 24 hours, starting in 2025)
scheduler.add_job(my_daily_task, trigger)
scheduler.start()

app = FastAPI()

# Ensure the scheduler shuts down properly on application exit.
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()

@app.get("/")
def read_root():
    return {"message": "FastAPI with APScheduler Demo"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
