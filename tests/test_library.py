import uuid
from fastapi import status

# def test_create_library(user):
#     response = user.post(
#         "/library",
#         json={
#             "name": "Libreria chevere",
#             "addres": "cra 99 No8 - 9"
#
#         }
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#


def test_show_library(user):
    response = user.get("/library/show")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert  isinstance(data,list)

def test_create_update_library(user):
    response = user.post(
        "/library",
        json={
            "name": "Libreria chevere",
            "addres": "cra 99 No8 - 9"

        }
    )
    id = response.json()["id"]


    response_update = user.patch(
        f"/library/update_id/{id}",
        json={
            "name": "Libreria chevere2",
            "addres": "cra 22 No2 - 2"

        }
    )
    assert response_update.status_code == status.HTTP_201_CREATED
    assert response_update.json()["name"] == "Libreria chevere2"