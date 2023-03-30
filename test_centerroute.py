# testing de los endpoints de center


from fastapi.testclient import TestClient
import json
from index import app
client = TestClient(app)


def test_get_centerExist():
    email_exist = 'info@spanishinstitute.net'
    email_not_exist = 'prueba@gmail.com'

    response = client.get('/api/get_center/'+email_exist)
    assert response.status_code == 200

    response = client.get('/api/get_center/'+email_not_exist)
    assert response.status_code == 400
    assert response.json()


def test_getAllCenters():
    data = {
        "name": "Universidad de pruebaaaa",
        "email": "prueba5@gmail.com",
        "type_center": "Universidad",
        "acronym": "UNI",
        "location": "Sevilla , España",
        "url_web": "www.pruebitaaaaa.com",
        "contact": "pruebi.com",
        "telefono": "76474484",
        "logo": "./public/center_images/prueba5@gmail.com/logo.png",
        "description": "es una prueba para ver si el codigo va"
    }
    response = client.get('/api/all_centers', json=data)
    assert response.status_code == 200
    assert data in response.json()


def test_addCenter():
    data = {
        "name": "Universidad me aburro",
        "email": "pruebacentrito@gmail.com",
        "type_center": "Universidad",
        "acronym": "UNI",
        "location": "Sevilla , España",
        "url_web": "www.pruebi.com",
        "contact": "pruebi.com",
        "telefono": "565654",
        "description": "pruebita nice"
    }
    response = client.post('/api/add_center', json=data)
    assert response.status_code == 200
   
