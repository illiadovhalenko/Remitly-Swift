from fastapi import FastAPI

from app.database import Base, engine, get_db
from app.models import SwiftCode
from app.api.endpoints import router as swift_router
from app.csv_parser import parse_and_load_swift_codes

Base.metadata.create_all(bind=engine)

app_main = FastAPI(title="SWIFT Codes API", version="1.0.0")

app_main.include_router(swift_router, prefix="/v1/swift-codes", tags=["swift-codes"])


@app_main.on_event("startup")
def startup_event():
    """
    start the session
    :return:
    """
    db = next(get_db())
    try:
        if not db.query(SwiftCode).first():
            parse_and_load_swift_codes(db, "app/swift_codes.csv")
    finally:
        db.close()


@app_main.get("/")
def read_root():
    return {"message": "SWIFT Codes API is running"}
