from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, services
from app.database import get_db

from typing import Union

router = APIRouter()


@router.get("/{swiftCode}", response_model=Union[schemas.SwiftCodeWithBranches, schemas.SwiftCodeBranch])
def read_swift_code(swiftCode: str, db: Session = Depends(get_db)):
    """
    Return information about a bank using swift code
    :param swiftCode: searched swift code
    :param db: Database session
    :return: Information about bank
    """
    db_swift = services.get_swift_code(db, swiftCode=swiftCode)
    if db_swift is None:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    return db_swift


@router.get("/country/{countryISO2}", response_model=schemas.CountrySwiftCodes)
def read_swift_codes_by_country(countryISO2: str, db: Session = Depends(get_db)):
    """
    Return information about a banks form given country
    :param countryISO2: country ISO2 code
    :param db: Database session
    :return: Information about banks
    """
    country_swift_codes = services.get_swift_codes_by_country(db, countryISO2=countryISO2)
    if country_swift_codes is None:
        raise HTTPException(status_code=404, detail="Country not found or no SWIFT codes for this country")
    return country_swift_codes


@router.post("/", response_model=schemas.MessageResponse)
def create_swift_code(swift_code: schemas.SwiftCodeCreate, db: Session = Depends(get_db)):
    """
    Add a new swift code to the database
    :param swift_code: json for new swift code
    :param db: Database session
    :return: message
    """
    existing_swift = services.get_swift_code(db, swift_code.swiftCode)
    if existing_swift:
        raise HTTPException(status_code=400, detail="SWIFT code already exists")

    services.create_swift_code(db=db, swiftCode=swift_code)
    return {"message": "SWIFT code created successfully"}


@router.delete("/{swiftCode}", response_model=schemas.MessageResponse)
def delete_swift_code(swiftCode: str, db: Session = Depends(get_db)):
    """
    Delete a swift code from the database
    :param swiftCode: swift code to delete
    :param db: Database session
    :return: message
    """
    success = services.delete_swift_code(db, swiftCode=swiftCode)
    if not success:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    return {"message": "SWIFT code deleted successfully"}