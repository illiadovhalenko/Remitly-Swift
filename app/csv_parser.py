import csv
from sqlalchemy.orm import Session
from app.models import SwiftCode


def parse_and_load_swift_codes(db: Session, file_path: str):
    """
    Convert csv file to Database with Swift Codes
    :param db: Database session
    :param file_path: path to csv file
    :return:
    """
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            isHeadquarter = row['SWIFT CODE'].endswith('XXX')

            branchOf = None
            if not isHeadquarter and not row['SWIFT CODE'].endswith('XXX'):
                branchOf = row['SWIFT CODE'][:8]

            swift_code = SwiftCode(
                swiftCode=row['SWIFT CODE'],
                bankName=row['NAME'],
                address=row['ADDRESS'],
                countryISO2=row['COUNTRY ISO2 CODE'].upper(),
                countryName=row['COUNTRY NAME'].upper(),
                isHeadquarter=isHeadquarter,
                branchOf=branchOf
            )

            db.add(swift_code)

        db.commit()
