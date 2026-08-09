import pytest

from app.utils.security import create_access_token
from tests.const import DATE_FROM, DATE_TO, PASSWORD_HASH


@pytest.fixture
async def booking(make_booking, room):
    return await make_booking(room)


@pytest.fixture
async def other_user_headers(db):
    other = await db.users.add(email="other@example.com", hashed_password=PASSWORD_HASH)
    await db.commit()
    return {"Authorization": f"Bearer {create_access_token(other.id)}"}


async def test_list_bookings(client, admin_headers, booking):
    resp = await client.get("/bookings/", headers=admin_headers)
    assert resp.status_code == 200

    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == booking.id
    assert data["items"][0]["cancelled_at"] is None


async def test_list_bookings_requires_admin(client, user_headers):
    resp = await client.get("/bookings/", headers=user_headers)
    assert resp.status_code == 403


async def test_get_my_bookings(client, user_headers, booking):
    resp = await client.get("/bookings/me", headers=user_headers)
    assert resp.status_code == 200

    data = resp.json()
    assert data["total"] == 1

    item = data["items"][0]
    assert item["id"] == booking.id
    assert item["room_id"] == booking.room_id
    assert item["price"] == booking.price
    assert item["total_cost"] == booking.price * 4
    assert item["status"] == "confirmed"


async def test_get_my_bookings_excludes_others(client, other_user_headers, booking):
    resp = await client.get("/bookings/me", headers=other_user_headers)
    assert resp.status_code == 200
    assert resp.json()["total"] == 0


async def test_create_booking(client, user_headers, user, room):
    resp = await client.post(
        "/bookings/",
        headers=user_headers,
        json={"room_id": room.id, "date_from": DATE_FROM, "date_to": DATE_TO},
    )
    assert resp.status_code == 201

    data = resp.json()
    assert data["user_id"] == user.id
    assert data["room_id"] == room.id
    assert data["price"] == room.price
    assert data["status"] == "confirmed"


async def test_create_booking_requires_auth(client, room):
    resp = await client.post(
        "/bookings/",
        json={"room_id": room.id, "date_from": DATE_FROM, "date_to": DATE_TO},
    )
    assert resp.status_code == 401


async def test_create_booking_room_not_found(client, user_headers):
    resp = await client.post(
        "/bookings/",
        headers=user_headers,
        json={"room_id": 9999, "date_from": DATE_FROM, "date_to": DATE_TO},
    )
    assert resp.status_code == 404


async def test_create_booking_room_full(client, user_headers, room, make_booking):
    for _ in range(room.quantity):
        await make_booking(room)

    resp = await client.post(
        "/bookings/",
        headers=user_headers,
        json={"room_id": room.id, "date_from": DATE_FROM, "date_to": DATE_TO},
    )
    assert resp.status_code == 409


async def test_create_booking_after_cancellation(
    client, user_headers, room, make_booking
):
    bookings = [await make_booking(room) for _ in range(room.quantity)]

    cancel = await client.post(
        f"/bookings/{bookings[0].id}/cancel", headers=user_headers
    )
    assert cancel.status_code == 200

    resp = await client.post(
        "/bookings/",
        headers=user_headers,
        json={"room_id": room.id, "date_from": DATE_FROM, "date_to": DATE_TO},
    )
    assert resp.status_code == 201


async def test_create_booking_date_in_past(client, user_headers, room):
    resp = await client.post(
        "/bookings/",
        headers=user_headers,
        json={"room_id": room.id, "date_from": "2020-01-01", "date_to": DATE_TO},
    )
    assert resp.status_code == 422


async def test_create_booking_invalid_date_range(client, user_headers, room):
    resp = await client.post(
        "/bookings/",
        headers=user_headers,
        json={"room_id": room.id, "date_from": DATE_TO, "date_to": DATE_FROM},
    )
    assert resp.status_code == 422


async def test_cancel_booking(client, user_headers, booking):
    resp = await client.post(f"/bookings/{booking.id}/cancel", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


async def test_cancel_booking_of_another_user(client, other_user_headers, booking):
    resp = await client.post(
        f"/bookings/{booking.id}/cancel", headers=other_user_headers
    )
    assert resp.status_code == 404


async def test_cancel_booking_admin_can_cancel_any(client, admin_headers, booking):
    resp = await client.post(f"/bookings/{booking.id}/cancel", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


async def test_cancel_booking_not_found(client, user_headers):
    resp = await client.post("/bookings/9999/cancel", headers=user_headers)
    assert resp.status_code == 404
