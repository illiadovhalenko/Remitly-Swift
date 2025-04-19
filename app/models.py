from sqlalchemy import Column, String, Boolean
from app.database import Base


class SwiftCode(Base):
    __tablename__ = "swift_codes"

    swiftCode = Column(String, primary_key=True, index=True)
    bankName = Column(String, index=True)
    address = Column(String)
    countryISO2 = Column(String, index=True)
    countryName = Column(String)
    isHeadquarter = Column(Boolean)
    branchOf = Column(String, index=True, nullable=True)

    def __repr__(self):
        return f"<SwiftCode {self.swiftCode} - {self.bankName}>"