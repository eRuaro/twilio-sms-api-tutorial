from twilio.rest import Client
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import os

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)


@app.get("/", status_code = status.HTTP_200_OK)
async def root():
    return {"message": "Hello!"}


@app.post("/message/send", status_code = status.HTTP_201_CREATED)
async def post_message(toNumber: str, fromNumber: str, message: str):
    if (toNumber == None or toNumber == "" or fromNumber == None or fromNumber == "" or message == None or message == ""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing values for query parameters")

    if (toNumber[0] != "+" or fromNumber[0] != "+"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Numbers must have a + sign in front")

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    clientMessage = client.messages.create(
        body=message,
        to=toNumber,
        from_=fromNumber,
    )

    return {
        "toNumber": toNumber,
        "fromNumber": fromNumber,
        "message": message,
        "messageBody": clientMessage.body
    }

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)
