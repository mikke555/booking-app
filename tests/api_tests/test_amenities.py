import pytest


@pytest.fixture
async def amenity(db):
    amenity = await db.amenities.add(name="Wi-Fi")
    await db.commit()
    return amenity


async def test_list_amenities(client, amenity):
    resp = await client.get("/amenities/")
    assert resp.status_code == 200
    assert [a["name"] for a in resp.json()] == ["Wi-Fi"]
