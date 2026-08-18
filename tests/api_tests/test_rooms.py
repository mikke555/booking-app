from tests.const import DATE_FROM, DATE_TO


async def test_list_rooms(client, room):
    resp = await client.get(
        f"/hotels/{room.hotel_id}/rooms",
        params={"date_from": DATE_FROM, "date_to": DATE_TO},
    )
    assert resp.status_code == 200
    assert resp.json() == [
        {
            "id": room.id,
            "hotel_id": room.hotel_id,
            "title": room.title,
            "description": room.description,
            "price": room.price,
            "amenities": [],
            "quantity_left": room.quantity,
        }
    ]


async def test_list_rooms_availability(client, room, make_booking):
    params = {"date_from": DATE_FROM, "date_to": DATE_TO}

    # A booking reduces quantity_left
    await make_booking(room)
    resp = await client.get(f"/hotels/{room.hotel_id}/rooms", params=params)
    assert resp.json()[0]["quantity_left"] == room.quantity - 1

    # A fully booked room drops out of the listing
    await make_booking(room)
    resp = await client.get(f"/hotels/{room.hotel_id}/rooms", params=params)
    assert resp.json() == []


async def test_list_rooms_hotel_not_found(client):
    resp = await client.get(
        "/hotels/9999/rooms", params={"date_from": DATE_FROM, "date_to": DATE_TO}
    )
    assert resp.status_code == 404


async def test_create_room(client, admin_headers, hotel, amenity):
    resp = await client.post(
        f"/hotels/{hotel.id}/rooms",
        headers=admin_headers,
        json={
            "title": "Double Room",
            "description": "Room with a double bed",
            "quantity": 1,
            "price": 250,
            "amenities_ids": [amenity.id],
        },
    )
    assert resp.status_code == 201

    data = resp.json()
    assert data["hotel_id"] == hotel.id
    assert data["title"] == "Double Room"
    assert data["quantity"] == 1
    assert data["price"] == 250
    assert [a["name"] for a in data["amenities"]] == ["Wi-Fi"]


async def test_create_room_unknown_amenity(client, admin_headers, hotel):
    resp = await client.post(
        f"/hotels/{hotel.id}/rooms",
        headers=admin_headers,
        json={
            "title": "Double Room",
            "quantity": 1,
            "price": 250,
            "amenities_ids": [9999],
        },
    )
    assert resp.status_code == 404


async def test_get_room(client, room):
    resp = await client.get(f"/rooms/{room.id}")
    assert resp.status_code == 200
    assert resp.json() == {
        "id": room.id,
        "hotel_id": room.hotel_id,
        "title": room.title,
        "description": room.description,
        "price": room.price,
        "quantity": room.quantity,
        "amenities": [],
    }


async def test_get_room_not_found(client):
    resp = await client.get("/rooms/9999")
    assert resp.status_code == 404


async def test_patch_room(client, admin_headers, room):
    resp = await client.patch(
        f"/rooms/{room.id}", headers=admin_headers, json={"price": 150}
    )
    assert resp.status_code == 200
    assert resp.json()["price"] == 150


async def test_clear_room_amenities(client, admin_headers, room, amenity):
    resp = await client.patch(
        f"/rooms/{room.id}", headers=admin_headers, json={"amenities_ids": [amenity.id]}
    )
    assert resp.status_code == 200

    resp = await client.patch(
        f"/rooms/{room.id}", headers=admin_headers, json={"amenities_ids": []}
    )
    assert resp.status_code == 200

    follow_up = await client.get(f"/rooms/{room.id}")
    assert follow_up.json()["amenities"] == []


async def test_delete_room(client, admin_headers, room):
    resp = await client.delete(f"/rooms/{room.id}", headers=admin_headers)
    assert resp.status_code == 204

    follow_up = await client.get(f"/rooms/{room.id}")
    assert follow_up.status_code == 404


async def test_delete_room_with_bookings(client, admin_headers, room, make_booking):
    await make_booking(room)

    resp = await client.delete(f"/rooms/{room.id}", headers=admin_headers)
    assert resp.status_code == 409
