from typing import List

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()


class EmailSchema(BaseModel):
    email: List[EmailStr]

val = os.getenv("MAIL_PASSWORD")
psswd = ''.join(chr(int(val[i:i+8], 2)) for i in range(0, len(val), 8))

conf = ConnectionConfig(
    MAIL_USERNAME ="fd1064",
    MAIL_PASSWORD = psswd,
    MAIL_FROM = "milde@hs-fulda.de",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.hs-fulda.de",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False
)

app = FastAPI()

html = """
<p>Thanks for using Fastapi-mail</p> 
"""

@app.get("/email/{text}")
async def simple_send(request:Request, text:str) -> JSONResponse:
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=["milde@hs-fulda.de"],
        body=f"""
            <h1>Kein Spam: ich teste, wie ich mit Python mails verschicken kann. :)</h1>
            <p>{text}</p>
            """,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})     


@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})     



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, workers=1)