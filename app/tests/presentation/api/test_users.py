from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_get_user(app: FastAPI, client: TestClient, faker: Faker) -> None:
    url = app.url_path_for("create_user")
    username = faker.name()
    response: Response = client.post(url, json={"name": username})
    assert response.status_code == 201
    assert response.json()["user_id"]
