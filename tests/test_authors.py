
from fastapi import status


def test_create_author(user):
    response = user.post(
        "/authors/",
        json={
            "name": "Gabriel García Márquez",
            "origin_country": "Colombia",
            "year": 1927
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Gabriel García Márquez"
    assert data["origin_country"] == "Colombia"
    assert data["year"] == 1927
    assert "id" in data



def test_show_all_authors(user):
    response = user.get("/authors/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

    assert len(data) > 0



def test_update_author(user):
    # crear un autor
    response_create = user.post(
        "/authors/",
        json={
            "name": "J.K. Rowling",
            "origin_country": "UK",
            "year": 1965
        },
    )
    author_id = response_create.json()["id"]

    # actualizar
    response_update = user.patch(
        f"/authors/{author_id}",
        json={
            "name": "Joanne Rowling",
            "origin_country": "United Kingdom",
            "year": 1965
        },
    )
    assert response_update.status_code == status.HTTP_201_CREATED
    updated_data = response_update.json()
    assert updated_data["name"] == "Joanne Rowling"
    assert updated_data["origin_country"] == "United Kingdom"



def test_delete_author(user):
    # Crear un autor para eliminar
    response_create = user.post(
        "/authors/",
        json={
            "name": "Ernest Hemingway",
            "origin_country": "USA",
            "year": 1899
        },
    )
    author_id = response_create.json()["id"]

    # eliminarlo
    response_delete = user.delete(f"/authors/{author_id}")
    assert response_delete.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]

    # eliminar de nuevo
    response_delete_again = user.delete(f"/authors/{author_id}")
    assert response_delete_again.status_code == status.HTTP_404_NOT_FOUND
