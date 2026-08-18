async def test_list_users(client, admin_headers, user):
    resp = await client.get("/users/", headers=admin_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2  # user + admin
    emails = [u["email"] for u in data["items"]]
    assert user.email in emails


async def test_get_me(client, user_headers, user):
    resp = await client.get("/users/me", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json() == {"id": user.id, "email": user.email, "is_active": True}


async def test_get_user(client, admin_headers, user):
    resp = await client.get(f"/users/{user.id}", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == user.email


async def test_get_user_not_found(client, admin_headers):
    resp = await client.get("/users/9999", headers=admin_headers)
    assert resp.status_code == 404


async def test_deactivate_user(client, admin_headers, user, user_headers):
    resp = await client.patch(
        f"/users/{user.id}", headers=admin_headers, json={"is_active": False}
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False

    follow_up = await client.get("/users/me", headers=user_headers)
    assert follow_up.status_code == 403
