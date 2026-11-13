import pytest 
from fastapi.testclient import TestClient 
from bookstore.main import app, books_db

client = TestClient(app)


def test_api_workflow():
    """Prueba integral de los flujos HTTP 201, 200, 204, 404 y 422."""
    books_db.clear()

    # 1. Test POST 201 Created
    payload = {
        "id": 101,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "year": 2008,
        "isbn": "978-0132350884",
    }
    res_post = client.post("/books", json=payload)
    assert res_post.status_code == 201
    assert res_post.json()["title"] == "Clean Code"

    # 2. Test GET 200 OK (all books and filter by author)
    res_get_all = client.get("/books")
    assert res_get_all.status_code == 200
    assert len(res_get_all.json()) == 1

    res_get_filter = client.get("/books?author=Robert C. Martin")
    assert res_get_filter.status_code == 200
    assert len(res_get_filter.json()) == 1
    assert res_get_filter.json()[0]["author"] == "Robert C. Martin"

    res_get_empty_filter = client.get("/books?author=Unknown Author")
    assert res_get_empty_filter.status_code == 200
    assert res_get_empty_filter.json() == []

    # 3. Test GET 200 OK by ID
    res_get = client.get("/books/101")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == 101

    # 4. Test GET 404 Not Found
    res_404 = client.get("/books/999")
    assert res_404.status_code == 404

    # 5. Test POST 422 Unprocessable Entity (Validación Pydantic: year < 1450 & short ISBN)
    invalid_payload = {
        "id": 102,
        "title": "Old Papyrus",
        "author": "Scribe",
        "year": 1200,  # Invalid year < 1450
        "isbn": "123",  # Short ISBN
    }
    res_422 = client.post("/books", json=invalid_payload)
    assert res_422.status_code == 422

    # 6. Test POST 422 Unprocessable Entity (year > 2026)
    future_payload = {
        "id": 103,
        "title": "Future Book",
        "author": "Futurist",
        "year": 2030,
        "isbn": "978-0132350884",
    }
    res_future_422 = client.post("/books", json=future_payload)
    assert res_future_422.status_code == 422

    # 7. Test POST 400 Bad Request (duplicate ID)
    res_dup = client.post("/books", json=payload)
    assert res_dup.status_code == 400

    # 8. Test DELETE 204 No Content
    res_del = client.delete("/books/101")
    assert res_del.status_code == 204
    assert res_del.text == ""

    # 9. Test DELETE 404 Not Found (deleting non-existent ID)
    res_del_404 = client.delete("/books/101")
    assert res_del_404.status_code == 404

    print("¡Todas las verificaciones de la API pasaron exitosamente!")


if __name__ == "__main__":
    test_api_workflow()
