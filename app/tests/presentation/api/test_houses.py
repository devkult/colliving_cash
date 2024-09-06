from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Response
import pytest


async def create_user(app: FastAPI, client: TestClient, faker: Faker) -> None:
    url = app.url_path_for("create_user")
    username = faker.name()
    user_create_response: Response = client.post(url, json={"name": username})
    user_id = user_create_response.json()["user_id"]
    assert user_id

    return user_id, username


async def create_house(
    app: FastAPI, client: TestClient, faker: Faker, user_id: str
) -> None:
    url = app.url_path_for("create_house")
    name = faker.name()
    house_create_response: Response = client.post(
        url, json={"name": name, "owner_id": user_id}
    )
    house_id = house_create_response.json()["house_id"]
    assert house_id

    return house_id, name


async def join_house(
    app: FastAPI, client: TestClient, faker: Faker, user_id: str, house_id: str
) -> None:
    url = app.url_path_for("join_house", house_id=house_id)
    response: Response = client.post(url, json={"user_id": user_id})
    assert response.status_code == 201
    resident_id = response.json()["resident_id"]
    assert resident_id
    return resident_id


@pytest.mark.asyncio
async def test_create_house(app: FastAPI, client: TestClient, faker: Faker) -> None:
    user_id, _ = await create_user(app, client, faker)
    await create_house(app, client, faker, user_id)


@pytest.mark.asyncio
async def test_create_house_with_non_existing_user(
    app: FastAPI, client: TestClient, faker: Faker
) -> None:
    url = app.url_path_for("create_house")
    name = faker.name()
    house_create_response: Response = client.post(
        url, json={"name": name, "owner_id": faker.uuid4()}
    )
    assert house_create_response.status_code == 404


@pytest.mark.asyncio
async def test_get_house(app: FastAPI, client: TestClient, faker: Faker) -> None:
    user_id, username = await create_user(app, client, faker)
    house_id, name = await create_house(app, client, faker, user_id)

    url = app.url_path_for("get_house", house_id=house_id)
    response: Response = client.get(url)
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["owner_id"] == user_id


@pytest.mark.asyncio
async def test_get_non_existing_house(
    app: FastAPI, client: TestClient, faker: Faker
) -> None:
    url = app.url_path_for("get_house", house_id=faker.uuid4())
    response: Response = client.get(url)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_join_house(app: FastAPI, client: TestClient, faker: Faker) -> None:
    user_id, _ = await create_user(app, client, faker)
    house_id, _ = await create_house(app, client, faker, user_id)

    await join_house(app, client, faker, user_id, house_id)


@pytest.mark.asyncio
async def test_join_non_existing_house(
    app: FastAPI, client: TestClient, faker: Faker
) -> None:
    url = app.url_path_for("join_house", house_id=faker.uuid4())
    response: Response = client.post(url, json={"user_id": faker.uuid4()})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_join_non_existing_user(
    app: FastAPI, client: TestClient, faker: Faker
) -> None:
    user_id, _ = await create_user(app, client, faker)
    house_id, _ = await create_house(app, client, faker, user_id)

    url = app.url_path_for("join_house", house_id=house_id)
    response: Response = client.post(url, json={"user_id": faker.uuid4()})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_house_residents(
    app: FastAPI, client: TestClient, faker: Faker
) -> None:
    user_id, _ = await create_user(app, client, faker)
    house_id, _ = await create_house(app, client, faker, user_id)

    resident_id = await join_house(app, client, faker, user_id, house_id)

    url = app.url_path_for("get_house_residents", house_id=house_id)
    response: Response = client.get(url)
    assert response.status_code == 200
    assert response.json()["residents"]

    assert resident_id in response.json()["residents"]
