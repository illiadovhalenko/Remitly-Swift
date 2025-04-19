import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app_main
from app.csv_parser import parse_and_load_swift_codes

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        parse_and_load_swift_codes(db, "./app/swift_codes.csv")
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app_main.dependency_overrides[get_db] = override_get_db
    yield TestClient(app_main)
    app_main.dependency_overrides.clear()


def test_read_swift_code_headquarter(client):
    response = client.get("/v1/swift-codes/BCHICLRMXXX")
    assert response.status_code == 200
    data = response.json()
    assert data["isHeadquarter"] is True
    assert len(data["branches"]) > 0
    assert data["swiftCode"] == "BCHICLRMXXX"


def test_read_swift_code_branch(client):
    response = client.get("/v1/swift-codes/BCHICLRMIOB")
    assert response.status_code == 200
    data = response.json()
    assert data["isHeadquarter"] is False
    assert "branches" not in data


def test_read_swift_code_not_found(client):
    response = client.get("/v1/swift-codes/NOTEXIST")
    assert response.status_code == 404


def test_read_swift_codes_by_country(client):
    response = client.get("/v1/swift-codes/country/PL")
    assert response.status_code == 200
    data = response.json()
    assert data["countryISO2"] == "PL"
    assert len(data["swiftCodes"]) > 0


def test_create_swift_code(client):
    swift_code_data = {
        "swiftCode": "TEST1234XXX",
        "bankName": "Test Bank",
        "address": "123 Test Street",
        "countryISO2": "US",
        "countryName": "United States",
        "isHeadquarter": True
    }
    response = client.post("/v1/swift-codes/", json=swift_code_data)
    assert response.status_code == 200
    assert response.json()["message"] == "SWIFT code created successfully"

    response = client.get("/v1/swift-codes/TEST1234XXX")
    assert response.status_code == 200
    assert response.json()["bankName"] == "Test Bank"


def test_delete_swift_code(client):
    swift_code_data = {
        "swiftCode": "TODEL123XXX",
        "bankName": "To Delete Bank",
        "address": "123 Delete Street",
        "countryISO2": "US",
        "countryName": "United States",
        "isHeadquarter": True
    }
    client.post("/v1/swift-codes/", json=swift_code_data)

    response = client.delete("/v1/swift-codes/TODEL123XXX")
    assert response.status_code == 200
    assert response.json()["message"] == "SWIFT code deleted successfully"

    response = client.get("/v1/swift-codes/TODEL123XXX")
    assert response.status_code == 404
