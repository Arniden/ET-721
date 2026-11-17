"""Tests for the NEW FEATURE: expiration dates on fruit."""
from datetime import datetime, timedelta, timezone

import pytest
from app import create_app
from app.models import Fruit, db


@pytest.fixture
def app_context():
    app = create_app({"TESTING": True})
    ctx = app.app_context()
    ctx.push()
    yield app
    db.session.remove()
    db.drop_all()
    ctx.pop()


def _utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ---- Validation / parsing ---------------------------------------------------

def test_createFruit_withoutExpirationDate_defaultsToNone():
    assert Fruit(name="Apple", quantity=1).expiration_date is None

def test_createFruit_withNoneExpirationDate_isAllowed():
    assert Fruit(name="Apple", quantity=1, expiration_date=None).expiration_date is None

def test_createFruit_withDatetimeExpirationDate_storesDatetime():
    expires = datetime(2030, 1, 15, 12, 0)
    fruit = Fruit(name="Apple", quantity=1, expiration_date=expires)
    assert fruit.expiration_date == expires

def test_createFruit_withIsoStringExpirationDate_parsesToDatetime():
    fruit = Fruit(name="Apple", quantity=1, expiration_date="2030-01-15T12:00:00")
    assert fruit.expiration_date == datetime(2030, 1, 15, 12, 0)

def test_createFruit_withDateOnlyString_parsesToMidnight():
    fruit = Fruit(name="Apple", quantity=1, expiration_date="2030-01-15")
    assert fruit.expiration_date == datetime(2030, 1, 15, 0, 0)

def test_createFruit_withZuluTimeString_convertsToNaiveUtc():
    fruit = Fruit(name="Apple", quantity=1, expiration_date="2030-01-15T12:00:00Z")
    assert fruit.expiration_date == datetime(2030, 1, 15, 12, 0)
    assert fruit.expiration_date.tzinfo is None

def test_createFruit_withUtcOffsetString_convertsToUtc():
    fruit = Fruit(name="Apple", quantity=1, expiration_date="2030-01-15T12:00:00+02:00")
    assert fruit.expiration_date == datetime(2030, 1, 15, 10, 0)

def test_createFruit_withTimezoneAwareDatetime_convertsToNaiveUtc():
    aware = datetime(2030, 1, 15, 12, 0, tzinfo=timezone(timedelta(hours=-5)))
    fruit = Fruit(name="Apple", quantity=1, expiration_date=aware)
    assert fruit.expiration_date == datetime(2030, 1, 15, 17, 0)

def test_createFruit_withInvalidDateString_raisesAssertionError():
    with pytest.raises(AssertionError, match="ISO 8601"):
        Fruit(name="Apple", quantity=1, expiration_date="not-a-date")

def test_createFruit_withNonDatetimeValue_raisesAssertionError():
    with pytest.raises(AssertionError, match="datetime"):
        Fruit(name="Apple", quantity=1, expiration_date=12345)

def test_serialize_withExpirationDate_returnsIsoString():
    fruit = Fruit(name="Apple", quantity=1, expiration_date=datetime(2030, 1, 15, 12, 0))
    assert fruit.serialize()['expiration_date'] == "2030-01-15T12:00:00"


# ---- is_expired -------------------------------------------------------------

def test_isExpired_withPastDate_returnsTrue():
    fruit = Fruit(name="Apple", quantity=1, expiration_date=datetime(2020, 1, 1))
    assert fruit.is_expired(now=datetime(2025, 1, 1)) is True

def test_isExpired_withFutureDate_returnsFalse():
    fruit = Fruit(name="Apple", quantity=1, expiration_date=datetime(2030, 1, 1))
    assert fruit.is_expired(now=datetime(2025, 1, 1)) is False

def test_isExpired_withNoExpirationDate_returnsFalse():
    assert Fruit(name="Apple", quantity=1).is_expired(now=datetime(2025, 1, 1)) is False

def test_isExpired_whenExactlyAtExpiration_returnsFalse():
    """Boundary: expired means strictly BEFORE now."""
    moment = datetime(2025, 1, 1, 12, 0)
    fruit = Fruit(name="Apple", quantity=1, expiration_date=moment)
    assert fruit.is_expired(now=moment) is False

def test_isExpired_withoutNowArgument_usesCurrentTime():
    yesterday = Fruit(name="Apple", quantity=1, expiration_date=_utc_now() - timedelta(days=1))
    tomorrow = Fruit(name="Pear", quantity=1, expiration_date=_utc_now() + timedelta(days=1))
    assert yesterday.is_expired() is True
    assert tomorrow.is_expired() is False


# ---- get_expired (database) -------------------------------------------------

def test_getExpired_withMixedFruits_returnsOnlyExpiredOnes(app_context):
    db.session.add_all([
        Fruit(name="Apple", quantity=1, expiration_date=datetime(2020, 1, 1)),
        Fruit(name="Banana", quantity=1, expiration_date=datetime(2030, 1, 1)),
        Fruit(name="Cherry", quantity=1),  # no expiration date
    ])
    db.session.commit()

    expired = Fruit.get_expired(now=datetime(2025, 6, 1))
    assert [fruit.name for fruit in expired] == ["Apple"]

def test_getExpired_withNoExpirationDates_returnsEmptyList(app_context):
    db.session.add(Fruit(name="Cherry", quantity=1))
    db.session.commit()
    assert Fruit.get_expired(now=datetime(2025, 6, 1)) == []

def test_getExpired_withoutNowArgument_usesCurrentTime(app_context):
    db.session.add_all([
        Fruit(name="Apple", quantity=1, expiration_date=datetime(2000, 1, 1)),
        Fruit(name="Banana", quantity=1, expiration_date=datetime(2999, 1, 1)),
    ])
    db.session.commit()
    assert [fruit.name for fruit in Fruit.get_expired()] == ["Apple"]

def test_expirationDate_whenSavedAndReloaded_isPreserved(app_context):
    db.session.add(Fruit(name="Apple", quantity=1, expiration_date="2030-01-15T12:00:00"))
    db.session.commit()
    db.session.expire_all()
    assert Fruit.query.first().expiration_date == datetime(2030, 1, 15, 12, 0)
