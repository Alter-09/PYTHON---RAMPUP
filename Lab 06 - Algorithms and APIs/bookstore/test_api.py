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

    # 2. Test GET 200 OK
    res_get = client.get("/books/101")
    assert res_get.status_code == 200

    # 3. Test GET 404 Not Found
    res_404 = client.get("/books/999")
    assert res_404.status_code == 404

    # 4. Test POST 422 Unprocessable Entity (Validación Pydantic)
    invalid_payload = {
        "id": 102,
        "title": "Old Papyrus",
        "author": "Scribe",
        "year": 1200,  # Año inválido < 1450
        "isbn": "123",  # ISBN corto
    }
    res_422 = client.post("/books", json=invalid_payload)
    assert res_422.status_code == 422

    # 5. Test DELETE 204 No Content
    res_del = client.delete("/books/101")
    assert res_del.status_code == 204
    assert res_del.text == ""

    print("¡Todas las verificaciones de la API pasaron exitosamente!")


if __name__ == "__main__":
    test_api_workflow()
