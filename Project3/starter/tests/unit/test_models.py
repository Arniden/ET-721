import pytest
from app.models import Fruit, FruitMetrics


def test_createFruit_withValidData_createsFruitWithCorrectAttributes():
    """
    Test the creation of a Fruit instance with valid parameters.
    Verifies that the name and quantity of the fruit are set correctly.
    """
    fruit = Fruit(name="Apple", quantity=10)
    assert fruit.name == "Apple"
    assert fruit.quantity == 10

def test_calculateTotalFruits_withFruitsList_returnsCorrectFruitCount():
    """
    Test the calculation of the total number of fruits in an inventory.
    Checks if the total_fruits method returns the correct count.
    """
    fruits = [Fruit(name="Apple", quantity=10), Fruit(name="Banana", quantity=5)]
    assert FruitMetrics.total_fruits(fruits) == 2

def test_calculateAverageQuantity_withFruitsList_returnsCorrectAverage():
    """
    Test the calculation of the average quantity of fruits in an inventory.
    Checks if the average_quantity method computes the correct average.
    """
    fruits = [
        Fruit(name="Apple", quantity=10),
        Fruit(name="Banana", quantity=20),
        Fruit(name="Cherry", quantity=30),
    ]
    assert FruitMetrics.average_quantity(fruits) == 20

def test_identifyMostCommonFruit_withFruitsList_returnsMostFrequentFruit():
    """
    Test to identify the most common fruit in an inventory.
    Checks if the most_common_fruit method correctly identifies the fruit that appears most frequently.
    """
    fruits = [
        Fruit(name="Apple", quantity=10),
        Fruit(name="Banana", quantity=5),
        Fruit(name="Apple", quantity=7),
    ]
    assert FruitMetrics.most_common_fruit(fruits) == "Apple"

def test_createFruit_withValidDetails_createsFruitSuccessfully():
    """
    Test the creation of a valid Fruit instance.
    Verifies that a fruit with valid name and quantity is created without errors.
    """
    valid_fruit = Fruit(name="Apple", quantity=10)
    assert valid_fruit.name == "Apple"
    assert valid_fruit.quantity == 10

def test_createFruit_withInvalidName_raisesAssertionError():
    """
    Test the creation of a Fruit instance with an invalid name.
    Verifies that an AssertionError is raised when the name is empty.
    """
    with pytest.raises(AssertionError):
        invalid_fruit = Fruit(name="", quantity=10)

def test_createFruit_withNegativeQuantity_raisesAssertionError():
    """
    Test the creation of a Fruit instance with an invalid quantity.
    Verifies that an AssertionError is raised when the quantity is negative.
    """
    with pytest.raises(AssertionError, match="non-negative"):
        Fruit(name="Apple", quantity=-1)

def test_createFruit_withNonIntegerQuantity_raisesAssertionError():
    """
    Test the creation of a Fruit instance with an invalid quantity type.
    Verifies that an AssertionError is raised when the quantity is not an integer.
    """
    with pytest.raises(AssertionError, match="integer"):
        Fruit(name="Apple", quantity="ten")

# ---------------------------------------------------------------------------
# Additional tests: edge cases and boundaries
# ---------------------------------------------------------------------------

def test_createFruit_withNoneName_raisesAssertionError():
    """A missing (None) name must be rejected with the 'required' message."""
    with pytest.raises(AssertionError, match="required"):
        Fruit(name=None, quantity=10)

def test_createFruit_withTwoCharacterName_raisesAssertionError():
    """Names must be MORE than 2 characters, so 2 is too short."""
    with pytest.raises(AssertionError, match="more than 2 characters"):
        Fruit(name="Ab", quantity=10)

def test_createFruit_withThreeCharacterName_createsFruitSuccessfully():
    """Boundary: 3 characters is the shortest valid name."""
    fruit = Fruit(name="Fig", quantity=1)
    assert fruit.name == "Fig"

def test_createFruit_withZeroQuantity_createsFruitSuccessfully():
    """Boundary: 0 is non-negative, so it is allowed (item out of stock)."""
    fruit = Fruit(name="Apple", quantity=0)
    assert fruit.quantity == 0

def test_createFruit_withFloatQuantity_raisesAssertionError():
    """A float is not an integer, even if it looks like a whole number."""
    with pytest.raises(AssertionError, match="integer"):
        Fruit(name="Apple", quantity=5.5)

def test_serialize_withFruit_returnsDictionaryOfAllFields():
    """serialize() should expose every field; unsaved fruit has no id yet."""
    fruit = Fruit(name="Apple", quantity=10, variety="Gala", season="Winter")
    assert fruit.serialize() == {
        'id': None,
        'name': 'Apple',
        'quantity': 10,
        'variety': 'Gala',
        'season': 'Winter',
        'expiration_date': None,
    }

def test_calculateTotalFruits_withEmptyList_returnsZero():
    assert FruitMetrics.total_fruits([]) == 0

def test_calculateTotalQuantity_withFruitsList_returnsSumOfQuantities():
    fruits = [Fruit(name="Apple", quantity=10), Fruit(name="Banana", quantity=5)]
    assert FruitMetrics.total_quantity(fruits) == 15

def test_calculateTotalQuantity_withEmptyList_returnsZero():
    assert FruitMetrics.total_quantity([]) == 0

def test_calculateAverageQuantity_withEmptyList_returnsZero():
    """Empty inventory must not cause a ZeroDivisionError."""
    assert FruitMetrics.average_quantity([]) == 0

def test_identifyMostCommonFruit_withEmptyList_returnsNone():
    assert FruitMetrics.most_common_fruit([]) is None

def test_identifyMostCommonFruit_withTie_returnsFirstFruitCounted():
    """With a tie, max() keeps the first fruit that reached the top count."""
    fruits = [Fruit(name="Banana", quantity=1), Fruit(name="Apple", quantity=1)]
    assert FruitMetrics.most_common_fruit(fruits) == "Banana"

def test_calculateAverageQuantityByFruit_withDuplicateNames_returnsAveragePerName():
    fruits = [
        Fruit(name="Apple", quantity=10),
        Fruit(name="Apple", quantity=20),
        Fruit(name="Banana", quantity=5),
    ]
    assert FruitMetrics.average_quantity_by_fruit(fruits) == {"Apple": 15, "Banana": 5}

def test_calculateAverageQuantityByFruit_withEmptyList_returnsEmptyDict():
    assert FruitMetrics.average_quantity_by_fruit([]) == {}
