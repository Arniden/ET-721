import pytest
from app import create_app
from app.models import Fruit, db


@pytest.fixture
def search_app():
    """
    A fresh app + empty in-memory database for EVERY test, pre-loaded with known data.
    Function scope (instead of module scope) means tests can't affect each other.
    """
    app = create_app({"TESTING": True})
    ctx = app.app_context()
    ctx.push()

    db.session.add_all([
        Fruit(name="Apple", quantity=10, variety="Gala", season="Winter"),
        Fruit(name="Banana", quantity=20, variety="Cavendish", season="All"),
        Fruit(name="Apple", quantity=15, variety="Fuji", season="Winter"),
        Fruit(name="Cherry", quantity=50, variety="Bing", season="Summer"),
        Fruit(name="Orange", quantity=5, variety="Navel", season="Fall"),
    ])
    db.session.commit()

    yield app

    db.session.remove()
    db.drop_all()
    ctx.pop()


def test_searchByName_withExistingFruitName_returnsFruitsWithName(search_app):
    """
    Test the search functionality by name in the Fruit model.
    Verifies that the search method returns the correct fruits when searching by name.
    """
    results = Fruit.search(name="Apple")
    assert len(results) == 2
    assert all(fruit.name == "Apple" for fruit in results)

def test_searchByName_withDifferentCase_isCaseInsensitive(search_app):
    results = Fruit.search(name="aPPle")
    assert len(results) == 2

def test_searchByName_withPartialName_returnsPartialMatches(search_app):
    results = Fruit.search(name="ana")
    assert [fruit.name for fruit in results] == ["Banana"]

def test_searchByVariety_withExistingVariety_returnsMatchingFruit(search_app):
    results = Fruit.search(variety="Gala")
    assert len(results) == 1
    assert results[0].name == "Apple"
    assert results[0].quantity == 10

def test_searchBySeason_withExistingSeason_returnsMatchingFruits(search_app):
    results = Fruit.search(season="Winter")
    assert len(results) == 2
    assert all(fruit.season == "Winter" for fruit in results)

def test_searchByMinQuantity_withMinimum_returnsFruitsAtOrAboveMinimum(search_app):
    results = Fruit.search(min_quantity=15)
    assert len(results) == 3  # Banana 20, Apple (Fuji) 15, Cherry 50
    assert all(fruit.quantity >= 15 for fruit in results)

def test_searchByMinQuantity_withZero_returnsEverything(search_app):
    """0 is falsy in Python; make sure it is still treated as a real filter value."""
    results = Fruit.search(min_quantity=0)
    assert len(results) == 5

def test_searchByMaxQuantity_withMaximum_returnsFruitsAtOrBelowMaximum(search_app):
    results = Fruit.search(max_quantity=10)
    assert len(results) == 2  # Apple (Gala) 10, Orange 5
    assert all(fruit.quantity <= 10 for fruit in results)

def test_searchByQuantityRange_withMinAndMax_returnsFruitsInsideRange(search_app):
    results = Fruit.search(min_quantity=10, max_quantity=20)
    assert sorted(fruit.quantity for fruit in results) == [10, 15, 20]

def test_searchWithMultipleFilters_withNameAndMinQuantity_returnsOnlyMatchingFruit(search_app):
    results = Fruit.search(name="Apple", min_quantity=15)
    assert len(results) == 1
    assert results[0].variety == "Fuji"

def test_searchWithNoFilters_returnsAllFruits(search_app):
    assert len(Fruit.search()) == 5

def test_searchWithNoMatches_returnsEmptyList(search_app):
    """
    Test the search does not return any results
    """
    assert Fruit.search(name="Mango") == []

def test_searchWithConflictingFilters_returnsEmptyList(search_app):
    """A name that exists but with a quantity range it does not satisfy yields nothing."""
    assert Fruit.search(name="Cherry", max_quantity=10) == []
