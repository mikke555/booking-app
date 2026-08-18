from app.utils.security import create_access_token
from tests.const import PASSWORD, PASSWORD_HASH


async def test_register(client):
    resp = await client.post(
        "/auth/register", json={"email": "new@example.com", "password": "password123"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert data["is_active"] is True
    assert "password" not in data and "hashed_password" not in data


async def test_register_duplicate_email(client, user):
    resp = await client.post(
        "/auth/register", json={"email": user.email, "password": "password123"}
    )
    assert resp.status_code == 409


async def test_login_returns_token(client, user):
    resp = await client.post(
        "/auth/token", data={"username": user.email, "password": PASSWORD}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


async def test_login_wrong_password(client, user):
    resp = await client.post(
        "/auth/token", data={"username": user.email, "password": "wrong-password"}
    )
    assert resp.status_code == 401


async def test_login_unknown_email(client):
    resp = await client.post(
        "/auth/token", data={"username": "ghost@example.com", "password": PASSWORD}
    )
    assert resp.status_code == 401


async def test_login_deactivated_user(client, db):
    await db.users.add(
        email="inactive@example.com", hashed_password=PASSWORD_HASH, is_active=False
    )
    await db.commit()

    resp = await client.post(
        "/auth/token", data={"username": "inactive@example.com", "password": PASSWORD}
    )
    assert resp.status_code == 403


async def test_protected_endpoint_requires_token(client):
    resp = await client.get("/bookings/me")
    assert resp.status_code == 401


async def test_invalid_token_rejected(client):
    resp = await client.get(
        "/bookings/me", headers={"Authorization": "Bearer not-a-jwt"}
    )
    assert resp.status_code == 401


async def test_token_for_nonexistent_user(client):
    headers = {"Authorization": f"Bearer {create_access_token(9999)}"}
    resp = await client.get("/users/me", headers=headers)
    assert resp.status_code == 401
