from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_basic_response():
    response = client.post("/api/honeypot", json={"message": {"text": "Hello"}})
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "reply" in data


def test_scam_message():
    msg = "Urgent! Send money to account 123456789"
    response = client.post("/api/honeypot", json={"message": {"text": msg}})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert "scam" in data["reply"].lower()


def test_safe_message():
    msg = "Hello, how are you?"
    response = client.post("/api/honeypot", json={"message": {"text": msg}})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert "not appear to be a scam" in data["reply"].lower()


def test_invalid_input():
    response = client.post("/api/honeypot", json={})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["reply"] == "Invalid input received."


def test_robustness():
    response = client.post("/api/honeypot", json={"message": {"text": "hi"}})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"


def run_tests():
    print("Running tests...")
    try:
        test_basic_response()
        print("Basic test passed.")
        
        test_scam_message()
        print("Scam test passed.")
        
        test_safe_message()
        print("Safe test passed.")
        
        test_invalid_input()
        print("Invalid input test passed.")
        
        test_robustness()
        print("Robustness test passed.")
        
        print("ALL TESTS PASSED.")
    except AssertionError as e:
        print(f"Test Failed: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_tests()
