import uuid

from fastapi import status
def test_create_user(user):
    response = user.post(
        "/users",
        json = {

            "name": "Jhon Doe",
            "email": "Jhon@library.com",
            "password": "123",
            "year": 2006,
            "rol": "reader"
        },

    )
    assert response.status_code == status.HTTP_201_CREATED

def test_read_one_user(user):
    response = user.post(
        "/users",
        json={

            "name": "Jhon Doe",
            "email": "Jhon@library.com",
            "password": "123",
            "year": 2006,
            "rol": "reader"
        },

    )
    assert response.status_code == status.HTTP_201_CREATED
    user_id: uuid.UUID = response.json()["id"]
    response_read = user.get(f"/users/{user_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == "Jhon Doe"

def test_show_all_users(user):
    response = user.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_show_active_users(user):

    response_active = user.get("/users/active")
    assert response_active.status_code == status.HTTP_200_OK
    assert isinstance(response_active.json(), list)

def test_show_inactive_users(user):

    response_inactive = user.get("/users/inactive")
    assert response_inactive.status_code == status.HTTP_200_OK
    assert isinstance(response_inactive.json(), list)

def test_update_user(user):
    # crear usuario
    response_create = user.post(
        "/users/",
        json={
            "name": "Alice",
            "email": "alice@library.com",
            "password": "xyz",
            "year": 2001,
            "rol": "reader"
        },
    )
    user_id = response_create.json()["id"]

    # actualizar
    response_update = user.patch(
        f"/users/update_id/{user_id}",
        json={"name": "Alice s",
            "email": "alice@librry.com",
            "password": "xy4",
            "year": 2002,
            "rol": "reader"},
    )
    assert response_update.status_code == status.HTTP_201_CREATED
    assert response_update.json()["name"] == "Alice s"
def test_delete_user(user):
    response_create = user.post(
        "/users/",
        json={
            "name": "Bob",
            "email": "bob@library.com",
            "password": "123",
            "year": 1999,
            "rol": "reader"
        },
    )
    user_id = response_create.json()["id"]

    response_delete = user.delete(f"/users/delete_user/{user_id}")
    assert response_delete.status_code in [status.HTTP_202_ACCEPTED, status.HTTP_200_OK]
def test_activate_user(user):
    response_create = user.post(
        "/users/",
        json={
            "name": "Carl",
            "email": "carl@library.com",
            "password": "123",
            "year": 1998,
            "rol": "reader"
        },
    )
    user_id = response_create.json()["id"]

    #  desactivar
    user.delete(f"/users/delete_user/{user_id}")

    # activar
    response_activate = user.patch(f"/users/active_user/{user_id}")
    assert response_activate.status_code in [status.HTTP_202_ACCEPTED, status.HTTP_200_OK]