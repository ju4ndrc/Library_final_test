from fastapi.testclient import TestClient
def  test_user(user):
    assert type(user) == TestClient