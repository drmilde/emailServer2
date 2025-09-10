from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from datetime import datetime
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from queue import Queue
import requests
from starlette.responses import JSONResponse
from typing import List
import os

from models import Email

## Variablen und Initialisierung
q = Queue()
load_dotenv()

val = os.getenv("MAIL_PASSWORD")
psswd = ''.join(chr(int(val[i:i+8], 2)) for i in range(0, len(val), 8))
username = os.getenv("MAIL_USERNAME")
srvername = os.getenv("MAIL_SERVER")

conf = ConnectionConfig(
    MAIL_USERNAME =username,
    MAIL_PASSWORD = psswd,
    MAIL_FROM = "WHO@SENDS-THE-MAIL.UK",
    MAIL_PORT = 587,
    MAIL_SERVER = srvername,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False
)

# Hier werden die emails versendet
def schedule_emails():
    print(f"EMAIL Task is running at {datetime.now()}")
    url = 'http://localhost:3000/sendmail'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.get(url)

# Der Scheduler wird konfiguriert
scheduler = BackgroundScheduler()
trigger = IntervalTrigger(seconds=10)
scheduler.add_job(schedule_emails, trigger)
scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print("STARTUP")
    yield
    # Clean up the ML models and release the resources
    print("SHUTDOWN")
    with q.mutex:
        q.queue.clear()
    scheduler.shutdown()


## Konfiguration der fastAPI app
app = FastAPI(lifespan=lifespan)

# ROUTEN

async def current_mail():
    if q.empty():
        return {}
    email = q.get()
    return email

async def schedule_current_mail():
    email = await current_mail()
    if email != {}:
        print(f"mail geht raus an: {email.mailaddress}")
        await sendmail(email)
    else:
        print("no mail to send")     

async def sendmail(email: Email):
    message = MessageSchema(
    subject=f"Geburtstag JT: Geschenk {email.id}",
    recipients=[f"{email.mailaddress}"],
    body=f'''
        <h1>Informationen zu dem ausgewählten Geschenk</h1>
        <p>Geschenk ID ist {email.id}</p>
        <p>Reserviert für {email.user}</p>
        <p>Bestellink: <a href="{email.url}">LINK</a></p>
        <p>Produktbezeichnung: {email.name}</p>
        <p>Produktbeschreibung: {email.description}</p>
        <p>Zusätzlicher Mailtext: {email.mailtext}</p>
        <p>Gesendet an: {email.mailaddress}</p>
        ''',
    subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

@app.get("/")
async def index():
    return {"message": "email schedule server"}

@app.get("/clear")
async def clear_queue():
    with q.mutex:
        q.queue.clear()
    return {"message": "queue cleared"}

@app.get("/email")
async def get_email():    
    email = await current_mail()
    return email

@app.post("/email")
async def add_email(email: Email):
    email.id = q.qsize()+1
    q.put_nowait(email)
    return {"message": f"email has been added to processing queue. ({q.qsize()})"}  


@app.get("/sendmail")
async def simple_send_get(request:Request) -> JSONResponse:
    await schedule_current_mail()
    return JSONResponse(status_code=200, content={"message": "email has been sent"})     


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, workers=1)

