from pydantic import BaseModel
from typing import List, Optional


class SwiftCodeBase(BaseModel):
    swiftCode: str
    bankName: str
    address: str
    countryISO2: str
    isHeadquarter: bool


class SwiftCodeCreate(SwiftCodeBase):
    countryName: Optional[str] = None


class SwiftCode(SwiftCodeBase):
    branchOf: Optional[str] = None
    countryName: Optional[str] = None


class SwiftCodeBranch(SwiftCodeBase):
    countryName: Optional[str] = None


class Branch(SwiftCodeBase):
    swiftCode: str


class SwiftCodeWithBranches(SwiftCodeBase):
    countryName: Optional[str] = None
    branches: Optional[List[Branch]] = None

    class Config:
        exclude_none = True


class CountrySwiftCodes(BaseModel):
    countryISO2: str
    countryName: str
    swiftCodes: List[SwiftCodeBase]


class MessageResponse(BaseModel):
    message: str
