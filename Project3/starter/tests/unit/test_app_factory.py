from sqlalchemy import inspect

from app import create_app
from app.models import db


class FakeConfig:
    TESTING = True
    CUSTOM_VALUE = "from-object"


def test_createApp_withoutConfig_usesInMemoryDatabaseDefaults():
    app = create_app()
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
    assert app.config['TESTING'] is False

def test_createApp_withDictConfig_appliesDictValues():
    app = create_app({"TESTING": True, "CUSTOM_VALUE": "from-dict"})
    assert app.config['TESTING'] is True
    assert app.config['CUSTOM_VALUE'] == "from-dict"

def test_createApp_withObjectConfig_appliesObjectValues():
    app = create_app(FakeConfig)
    assert app.config['TESTING'] is True
    assert app.config['CUSTOM_VALUE'] == "from-object"

def test_createApp_registersMainBlueprint():
    assert 'main' in create_app().blueprints

def test_createApp_createsFruitTable():
    app = create_app()
    with app.app_context():
        assert inspect(db.engine).has_table('fruit')
