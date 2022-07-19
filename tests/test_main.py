from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello!"}

def test_post_message():
    toNumber = "00"
    fromNumber = "01"
    message = "Hello, from Twilio and Python!"
    response = client.post("/message/send?toNumber=" + toNumber + "&fromNumber=" + fromNumber + "&message=" + message)
    assert response.status_code == 201
    assert response.json() == {
        "toNumber": toNumber,
        "fromNumber": fromNumber, 
        "message": message
    }
