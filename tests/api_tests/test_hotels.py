from tests.const import DATE_FROM, DATE_TO


async def test_list_hotels_excludes_hotel_without_rooms(client, hotel):
    resp = await client.get(
        "/hotels/", params={"date_from": DATE_FROM, "date_to": DATE_TO}
    )
    assert resp.status_code == 200
    assert resp.json()["total"] == 0


async def test_list_hotels_requires_dates(client):
    resp = await client.get("/hotels/")
    assert resp.status_code == 422


async def test_list_hotels(client, hotel, room):
    resp = await client.get(
        "/hotels/", params={"date_from": DATE_FROM, "date_to": DATE_TO}
    )
    assert resp.status_code == 200

    data = resp.json()
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["per_page"] == 10
    assert data["items"] == [
        {
            "id": hotel.id,
            "name": hotel.name,
            "location": hotel.location,
        }
    ]


async def test_create_hotel(client, admin_headers):
    resp = await client.post(
        "/hotels/",
        headers=admin_headers,
        json={"name": "Velvet Caviar Luxury Suites", "location": "Michigan"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Velvet Caviar Luxury Suites"
    assert data["location"] == "Michigan"


async def test_create_hotel_requires_admin(client, user_headers):
    resp = await client.post(
        "/hotels/",
        headers=user_headers,
        json={"name": "Velvet Caviar Luxury Suites", "location": "Michigan"},
    )
    assert resp.status_code == 403


async def test_get_hotel(client, hotel):
    resp = await client.get(f"/hotels/{hotel.id}")
    assert resp.status_code == 200
    assert resp.json() == {
        "id": hotel.id,
        "name": hotel.name,
        "location": hotel.location,
    }


async def test_patch_hotel(client, admin_headers, hotel):
    resp = await client.patch(
        f"/hotels/{hotel.id}",
        headers=admin_headers,
        json={"name": "Unaffordable Palace"},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Unaffordable Palace"


async def test_delete_hotel(client, admin_headers, hotel):
    resp = await client.delete(f"/hotels/{hotel.id}", headers=admin_headers)
    assert resp.status_code == 204

    follow_up = await client.get(f"/hotels/{hotel.id}")
    assert follow_up.status_code == 404
