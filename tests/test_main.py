from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello!"}

def test_post_message_success():
    toNumber = "%2B639692956701"
    fromNumber = "%2B19706388875"
    toNumberExpected = "+639692956701"
    fromNumberExpected = "+19706388875"
    message = "Hello, from Twilio and Python!"
    messageBodyExpected = "Sent from your Twilio trial account - Hello, from Twilio and Python!"
    
    response = client.post("/message/send?toNumber=" + toNumber + "&fromNumber=" + fromNumber + "&message=" + message)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "toNumber": toNumberExpected,
        "fromNumber": fromNumberExpected,
        "message": message,
        "messageBody": messageBodyExpected,
    }

def test_post_message_missing_all_query_parameters():
    response = client.post("/message/send")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_post_message_missing_query_parameter():
    response = client.post("/message/send?fromNumber=01&message=Hello, from Twilio and Python!")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_post_message_missing_values_query_parameters():
    response = client.post("/message/send?toNumber=&fromNumber=&message=")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing values for query parameters"}

def test_post_message_missing_sign_from_number():
    response = client.post("/message/send?toNumber=00&fromNumber=01&message=Hello, from Twilio and Python!")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Numbers must have a + sign in front"}