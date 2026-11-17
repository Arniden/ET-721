import json
from datetime import datetime

import pytest
from app import create_app
from app.models import db, Fruit

@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        # Put some initial data into the database
        # (Apple is already expired, Banana expires far in the future)
        fruits = [
            Fruit(name="Apple", quantity=10, variety="Gala", season="Winter",
                  expiration_date=datetime(2020, 1, 1)),
            Fruit(name="Banana", quantity=20, variety="Cavendish", season="All",
                  expiration_date=datetime(2999, 1, 1)),
        ]
        db.session.bulk_save_objects(fruits)
        db.session.commit()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def _names(response):
    return [fruit['name'] for fruit in response.get_json()]

# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

def test_home_returnsDocumentationMessage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'documentation' in response.get_json()['message']

# ---------------------------------------------------------------------------
# GET all / POST
# ---------------------------------------------------------------------------

def test_getAllFruits_whenDatabaseHasFruits_returnsFruitsList(client):
    """
    Test fetching all fruits from the database
    Validates that the GET request to '/api/fruits' returns a 200 status code,
    the correct number of fruits, and specific data of the fruits
    """
    response = client.get('/api/fruits')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 2  # Adjust based on your initial data
    assert data[0]['name'] == 'Apple'

def test_addFruit_withValidData_returnsSuccessMessageAndFruitId(client):
    """
    Test adding a new fruit to the database
    Validates that the POST request to '/api/fruits' adds the fruit correctly,
    and returns a 201 status code along with a success message and the fruit's ID
    """
    new_fruit = {"name": "Orange", "quantity": 5, "variety": "Navel", "season": "Winter"}
    response = client.post('/api/fruits', json=new_fruit)
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['message'] == 'Fruit added successfully'
    assert 'id' in data

def test_addFruit_withValidData_fruitAppearsInInventory(client):
    client.post('/api/fruits', json={"name": "Orange", "quantity": 5, "variety": "Navel", "season": "Winter"})
    assert _names(client.get('/api/fruits')) == ["Apple", "Banana", "Orange"]

def test_addFruit_withExpirationDate_storesAndReturnsIt(client):
    client.post('/api/fruits', json={"name": "Mango", "quantity": 3, "expiration_date": "2030-05-01T08:30:00"})
    mango = client.get('/api/fruits').get_json()[-1]
    assert mango['name'] == "Mango"
    assert mango['expiration_date'] == "2030-05-01T08:30:00"

def test_addFruit_withOnlyRequiredFields_succeedsWithNullOptionals(client):
    response = client.post('/api/fruits', json={"name": "Mango", "quantity": 3})
    assert response.status_code == 201
    mango = client.get('/api/fruits').get_json()[-1]
    assert mango['variety'] is None
    assert mango['season'] is None
    assert mango['expiration_date'] is None

def test_addFruit_withMissingName_returns400(client):
    response = client.post('/api/fruits', json={"quantity": 5})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Name is required'

def test_addFruit_withTooShortName_returns400(client):
    response = client.post('/api/fruits', json={"name": "Ab", "quantity": 5})
    assert response.status_code == 400
    assert 'more than 2 characters' in response.get_json()['message']

def test_addFruit_withNegativeQuantity_returns400(client):
    response = client.post('/api/fruits', json={"name": "Orange", "quantity": -1})
    assert response.status_code == 400
    assert 'non-negative' in response.get_json()['message']

def test_addFruit_withStringQuantity_returns400(client):
    response = client.post('/api/fruits', json={"name": "Orange", "quantity": "5"})
    assert response.status_code == 400
    assert 'integer' in response.get_json()['message']

def test_addFruit_withMissingQuantity_returns400(client):
    response = client.post('/api/fruits', json={"name": "Orange"})
    assert response.status_code == 400
    assert 'integer' in response.get_json()['message']

def test_addFruit_withInvalidExpirationDate_returns400(client):
    response = client.post('/api/fruits', json={"name": "Orange", "quantity": 5, "expiration_date": "tomorrow"})
    assert response.status_code == 400
    assert 'ISO 8601' in response.get_json()['message']

def test_addFruit_withInvalidData_doesNotChangeInventory(client):
    client.post('/api/fruits', json={"name": "Ab", "quantity": 5})
    assert len(client.get('/api/fruits').get_json()) == 2

# ---------------------------------------------------------------------------
# PUT
# ---------------------------------------------------------------------------

def test_updateFruit_withQuantityOnly_changesQuantityAndKeepsOtherFields(client):
    response = client.put('/api/fruits/1', json={"quantity": 99})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Fruit updated successfully'

    apple = client.get('/api/fruits').get_json()[0]
    assert apple['quantity'] == 99
    assert apple['name'] == "Apple"
    assert apple['variety'] == "Gala"
    assert apple['season'] == "Winter"

def test_updateFruit_withAllFields_updatesEveryField(client):
    new_values = {"name": "Pear", "quantity": 7, "variety": "Bartlett", "season": "Fall",
                  "expiration_date": "2031-02-03T04:05:06"}
    response = client.put('/api/fruits/1', json=new_values)
    assert response.status_code == 200

    pear = client.get('/api/fruits').get_json()[0]
    assert pear['name'] == "Pear"
    assert pear['quantity'] == 7
    assert pear['variety'] == "Bartlett"
    assert pear['season'] == "Fall"
    assert pear['expiration_date'] == "2031-02-03T04:05:06"

def test_updateFruit_withNonExistentId_returns404(client):
    response = client.put('/api/fruits/999', json={"quantity": 5})
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Fruit not found'

def test_updateFruit_withNegativeQuantity_returns400AndKeepsOldValue(client):
    response = client.put('/api/fruits/1', json={"quantity": -5})
    assert response.status_code == 400
    assert 'non-negative' in response.get_json()['message']
    assert client.get('/api/fruits').get_json()[0]['quantity'] == 10

def test_updateFruit_withInvalidName_returns400AndKeepsOldName(client):
    response = client.put('/api/fruits/1', json={"name": "Ab"})
    assert response.status_code == 400
    assert client.get('/api/fruits').get_json()[0]['name'] == "Apple"

def test_updateFruit_withNullExpirationDate_clearsExpirationDate(client):
    response = client.put('/api/fruits/1', json={"expiration_date": None})
    assert response.status_code == 200
    assert client.get('/api/fruits').get_json()[0]['expiration_date'] is None

# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------

def test_deleteFruit_withExistingId_removesFruit(client):
    response = client.delete('/api/fruits/1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Fruit deleted successfully'
    assert _names(client.get('/api/fruits')) == ["Banana"]

def test_deleteFruit_withNonExistentId_returns404(client):
    response = client.delete('/api/fruits/999')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Fruit not found'
    assert len(client.get('/api/fruits').get_json()) == 2

def test_deleteFruit_calledTwice_secondCallReturns404(client):
    assert client.delete('/api/fruits/1').status_code == 200
    assert client.delete('/api/fruits/1').status_code == 404

# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def test_searchFruits_byName_returnsMatchingFruit(client):
    response = client.get('/api/fruits/search?name=Apple')
    assert response.status_code == 200
    assert _names(response) == ["Apple"]

def test_searchFruits_byVarietyIgnoringCase_returnsMatchingFruit(client):
    assert _names(client.get('/api/fruits/search?variety=cavendish')) == ["Banana"]

def test_searchFruits_bySeason_returnsMatchingFruit(client):
    assert _names(client.get('/api/fruits/search?season=winter')) == ["Apple"]

def test_searchFruits_byMinQuantity_returnsFruitsAtOrAboveMinimum(client):
    assert _names(client.get('/api/fruits/search?min_quantity=20')) == ["Banana"]

def test_searchFruits_byMaxQuantity_returnsFruitsAtOrBelowMaximum(client):
    assert _names(client.get('/api/fruits/search?max_quantity=10')) == ["Apple"]

def test_searchFruits_withNameAndMinQuantity_combinesFilters(client):
    assert _names(client.get('/api/fruits/search?name=Banana&min_quantity=15')) == ["Banana"]
    response = client.get('/api/fruits/search?name=Apple&min_quantity=15')
    assert response.get_json() == {'message': 'No fruits found matching the search criteria'}

def test_searchFruits_withNoMatches_returnsNotFoundMessageWith200(client):
    response = client.get('/api/fruits/search?name=Mango')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'No fruits found matching the search criteria'}

def test_searchFruits_withNoParameters_returnsAllFruits(client):
    assert len(client.get('/api/fruits/search').get_json()) == 2

def test_searchFruits_withNonNumericMinQuantity_ignoresTheFilter(client):
    """Flask's type=int silently returns None for garbage, so the filter is skipped."""
    assert len(client.get('/api/fruits/search?min_quantity=abc').get_json()) == 2

# ---------------------------------------------------------------------------
# NEW FEATURE: expired produce
# ---------------------------------------------------------------------------

def test_getExpiredFruits_returnsOnlyExpiredFruit(client):
    response = client.get('/api/fruits/expired')
    assert response.status_code == 200
    data = response.get_json()
    assert [fruit['name'] for fruit in data] == ["Apple"]
    assert data[0]['expiration_date'] == "2020-01-01T00:00:00"

def test_getExpiredFruits_whenNothingExpired_returnsEmptyList(client):
    client.delete('/api/fruits/1')  # remove the expired Apple
    response = client.get('/api/fruits/expired')
    assert response.status_code == 200
    assert response.get_json() == []

def test_getExpiredFruits_afterAddingPastDatedFruit_includesNewFruit(client):
    client.post('/api/fruits', json={"name": "Mango", "quantity": 3, "expiration_date": "2000-01-01"})
    assert set(_names(client.get('/api/fruits/expired'))) == {"Apple", "Mango"}

def test_getExpiredFruits_afterExtendingExpiration_noLongerReturnsFruit(client):
    client.put('/api/fruits/1', json={"expiration_date": "2999-12-31"})
    assert client.get('/api/fruits/expired').get_json() == []

def test_getExpiredFruits_ignoresFruitWithoutExpirationDate(client):
    client.post('/api/fruits', json={"name": "Mango", "quantity": 3})
    assert _names(client.get('/api/fruits/expired')) == ["Apple"]

# ---------------------------------------------------------------------------
# NEW FEATURE: analytics
# ---------------------------------------------------------------------------

def test_getAnalytics_withInitialData_returnsCorrectMetrics(client):
    response = client.get('/api/fruits/analytics')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_fruits'] == 2
    assert data['total_quantity'] == 30
    assert data['average_quantity'] == 15
    assert data['most_common_fruit'] == "Apple"  # tie -> first one counted
    assert data['average_quantity_by_fruit'] == {"Apple": 10, "Banana": 20}

def test_getAnalytics_withDuplicateNames_countsAndAveragesPerName(client):
    client.post('/api/fruits', json={"name": "Banana", "quantity": 40})
    data = client.get('/api/fruits/analytics').get_json()
    assert data['total_fruits'] == 3
    assert data['total_quantity'] == 70
    assert data['most_common_fruit'] == "Banana"
    assert data['average_quantity_by_fruit']["Banana"] == 30

def test_getAnalytics_withEmptyInventory_returnsZerosAndNull(client):
    client.delete('/api/fruits/1')
    client.delete('/api/fruits/2')
    response = client.get('/api/fruits/analytics')
    assert response.status_code == 200
    assert response.get_json() == {
        'total_fruits': 0,
        'total_quantity': 0,
        'average_quantity': 0,
        'most_common_fruit': None,
        'average_quantity_by_fruit': {},
    }
