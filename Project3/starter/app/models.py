from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


def _utc_now():
    """Current UTC time as a naive datetime (SQLite stores naive datetimes)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    variety = db.Column(db.String(80))
    season = db.Column(db.String(80))
    # NEW FEATURE: when the produce expires (optional)
    expiration_date = db.Column(db.DateTime, nullable=True)

    # The `validates` decorator from SQLAlchemy is used for validation logic
    # When creating or modifying Fruit instance, it will automatically be called
    # and will raise an AssertionError if it cannot validate
    @validates('name')
    def validate_name(self, key, name):
        assert name, 'Name is required'
        assert len(name) > 2, 'Name must be more than 2 characters'
        return name

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        assert isinstance(quantity, int), 'Quantity must be an integer'
        assert quantity >= 0, 'Quantity must be non-negative'
        return quantity

    @validates('expiration_date')
    def validate_expiration_date(self, key, value):
        """Accepts None, a datetime, or an ISO 8601 string. Stored as naive UTC."""
        if value is None:
            return None
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                raise AssertionError('Expiration date must be a valid ISO 8601 date')
        assert isinstance(value, datetime), 'Expiration date must be a datetime'
        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    def is_expired(self, now=None):
        """True only if an expiration date is set and it is strictly before `now`."""
        if self.expiration_date is None:
            return False
        now = now or _utc_now()
        return self.expiration_date < now

    @staticmethod
    def get_expired(now=None):
        """All fruits whose expiration date is set and earlier than `now`."""
        now = now or _utc_now()
        return Fruit.query.filter(
            Fruit.expiration_date.isnot(None),
            Fruit.expiration_date < now
        ).all()

    @staticmethod
    def search(name=None, variety=None, season=None, min_quantity=None, max_quantity=None):
        query = Fruit.query
        if name:
            query = query.filter(Fruit.name.ilike(f'%{name}%'))
        if variety:
            query = query.filter(Fruit.variety.ilike(f'%{variety}%'))
        if season:
            query = query.filter(Fruit.season.ilike(f'%{season}%'))
        if min_quantity is not None:
            query = query.filter(Fruit.quantity >= min_quantity)
        if max_quantity is not None:
            query = query.filter(Fruit.quantity <= max_quantity)
        return query.all()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'variety': self.variety,
            'season': self.season,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None
        }

class FruitMetrics:
    @staticmethod
    def total_fruits(fruits):
        return len(fruits)

    @staticmethod
    def total_quantity(fruits):
        return sum(fruit.quantity for fruit in fruits)

    @staticmethod
    def average_quantity(fruits):
        if not fruits:
            return 0
        return sum(fruit.quantity for fruit in fruits) / len(fruits)

    @staticmethod
    def average_quantity_by_fruit(fruits):
        totals = {}
        counts = {}
        for fruit in fruits:
            totals[fruit.name] = totals.get(fruit.name, 0) + fruit.quantity
            counts[fruit.name] = counts.get(fruit.name, 0) + 1
        return {name: totals[name] / counts[name] for name in totals}

    @staticmethod
    def most_common_fruit(fruits):
        if not fruits:
            return None
        fruit_counts = {}
        for fruit in fruits:
            fruit_counts[fruit.name] = fruit_counts.get(fruit.name, 0) + 1
        return max(fruit_counts, key=fruit_counts.get)
