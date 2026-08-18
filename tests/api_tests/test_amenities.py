async def test_list_amenities(client, amenity):
    resp = await client.get("/amenities/")
    assert resp.status_code == 200
    titles = [a["name"] for a in resp.json()]
    assert "Wi-Fi" in titles


async def test_create_amenity(client, admin_headers):
    resp = await client.post(
        "/amenities/", headers=admin_headers, json={"name": "Pool"}
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Pool"


async def test_create_amenity_requires_admin(client, user_headers):
    resp = await client.post("/amenities/", headers=user_headers, json={"name": "Pool"})
    assert resp.status_code == 403


async def test_create_amenity_duplicate(client, admin_headers, amenity):
    resp = await client.post(
        "/amenities/", headers=admin_headers, json={"name": amenity.name}
    )
    assert resp.status_code == 409


async def test_get_amenity(client, amenity):
    resp = await client.get(f"/amenities/{amenity.id}")
    assert resp.status_code == 200
    assert resp.json() == {"id": amenity.id, "name": amenity.name}


async def test_get_amenity_not_found(client):
    resp = await client.get("/amenities/9999")
    assert resp.status_code == 404


async def test_update_amenity_duplicate(client, admin_headers, amenity, db):
    other = await db.amenities.add(name="Pool")
    await db.commit()

    resp = await client.put(
        f"/amenities/{other.id}", headers=admin_headers, json={"name": amenity.name}
    )
    assert resp.status_code == 409


async def test_update_amenity(client, admin_headers, amenity):
    resp = await client.put(
        f"/amenities/{amenity.id}", headers=admin_headers, json={"name": "Wi-Fi 6"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"id": amenity.id, "name": "Wi-Fi 6"}


async def test_delete_amenity(client, admin_headers, amenity):
    resp = await client.delete(f"/amenities/{amenity.id}", headers=admin_headers)
    assert resp.status_code == 204

    follow_up = await client.get(f"/amenities/{amenity.id}")
    assert follow_up.status_code == 404


async def test_delete_amenity_attached_to_room(client, admin_headers, room, amenity):
    resp = await client.patch(
        f"/rooms/{room.id}",
        headers=admin_headers,
        json={"amenities_ids": [amenity.id]},
    )
    assert resp.status_code == 200

    resp = await client.delete(f"/amenities/{amenity.id}", headers=admin_headers)
    assert resp.status_code == 204

    follow_up = await client.get(f"/rooms/{room.id}")
    assert follow_up.status_code == 200
    assert follow_up.json()["amenities"] == []
