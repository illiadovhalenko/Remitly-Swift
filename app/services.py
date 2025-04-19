from sqlalchemy.orm import Session

from app import models
from app import schemas


def get_swift_code(db: Session, swiftCode: str):
    db_swift = db.query(models.SwiftCode).filter(models.SwiftCode.swiftCode == swiftCode).first()

    if not db_swift:
        return None

    if db_swift.isHeadquarter:
        branches = db.query(models.SwiftCode).filter(
            models.SwiftCode.branchOf.startswith(db_swift.swiftCode[:8]),
            models.SwiftCode.swiftCode != db_swift.swiftCode
        ).all()
        swift_with_branches = schemas.SwiftCodeWithBranches(
            **db_swift.__dict__,
            branches=[schemas.Branch(**branch.__dict__) for branch in branches]
        )
        return swift_with_branches
    else:
        return schemas.SwiftCodeBranch(**db_swift.__dict__)


def get_swift_codes_by_country(db: Session, countryISO2: str):
    country_swift_codes = db.query(models.SwiftCode).filter(
        models.SwiftCode.countryISO2.startswith(countryISO2.upper())
    ).all()
    print(type(country_swift_codes))
    if not country_swift_codes:
        return None

    countryName = country_swift_codes[0].countryName

    return schemas.CountrySwiftCodes(
        countryISO2=countryISO2.upper(),
        countryName=countryName,
        swiftCodes=[schemas.SwiftCodeBase(**swiftcodes.__dict__) for swiftcodes in country_swift_codes]
    )


def create_swift_code(db: Session, swiftCode: schemas.SwiftCodeCreate):
    isBranch = not swiftCode.isHeadquarter and not swiftCode.swiftCode.endswith("XXX")

    branchOf = None
    if isBranch:
        branchOf = swiftCode.swift_code[:8]

    db_swift = models.SwiftCode(
        swiftCode=swiftCode.swiftCode,
        bankName=swiftCode.bankName,
        address=swiftCode.address,
        countryISO2=swiftCode.countryISO2.upper(),
        countryName=swiftCode.countryName.upper(),
        isHeadquarter=swiftCode.isHeadquarter,
        branchOf=branchOf
    )
    db.add(db_swift)
    db.commit()
    db.refresh(db_swift)
    return db_swift


def delete_swift_code(db: Session, swiftCode: str):
    db_swift = db.query(models.SwiftCode).filter(models.SwiftCode.swiftCode == swiftCode).first()
    if not db_swift:
        return False

    db.delete(db_swift)
    db.commit()
    return True
