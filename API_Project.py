from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import date, time

app = FastAPI(title="Birth Certificate Database API")

# In-memory database
birth_certificates = {}


# --- Data Model ---
class BirthCertificate(BaseModel):
    child_name: str
    mother_name: str
    father_name: str
    place_of_birth: str
    time_of_birth: str   # e.g. "14:35"
    date_of_birth: str   # e.g. "2024-03-15"


class BirthCertificateUpdate(BaseModel):
    child_name: Optional[str] = None
    mother_name: Optional[str] = None
    father_name: Optional[str] = None
    place_of_birth: Optional[str] = None
    time_of_birth: Optional[str] = None
    date_of_birth: Optional[str] = None


# --- Routes ---

@app.get("/")
def home():
    return {"message": "Birth Certificate Database API is running"}


@app.get("/certificates")
def get_all_certificates():
    """Return all birth certificates."""
    return list(birth_certificates.values())


@app.get("/certificates/{certificate_id}")
def get_certificate(certificate_id: str):
    """Return a single certificate by unique ID."""
    if certificate_id not in birth_certificates:
        raise HTTPException(status_code=404, detail=f"Certificate ID '{certificate_id}' not found")
    return birth_certificates[certificate_id]


@app.post("/certificates")
def create_certificate(data: BirthCertificate):
    """Create a new birth certificate and return its unique ID."""
    certificate_id = str(uuid.uuid4())
    record = {
        "id": certificate_id,
        **data.dict()
    }
    birth_certificates[certificate_id] = record
    return {"message": "Birth certificate created", "id": certificate_id, "data": record}


@app.put("/certificates/{certificate_id}")
def update_certificate(certificate_id: str, data: BirthCertificateUpdate):
    """Update one or more fields of an existing certificate by ID."""
    if certificate_id not in birth_certificates:
        raise HTTPException(status_code=404, detail=f"Certificate ID '{certificate_id}' not found")

    existing = birth_certificates[certificate_id]
    updates = data.dict(exclude_none=True)   # Only update fields that were provided

    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    existing.update(updates)
    birth_certificates[certificate_id] = existing
    return {"message": "Certificate updated", "data": existing}


@app.delete("/certificates/{certificate_id}")
def delete_certificate(certificate_id: str):
    """Delete a certificate by unique ID."""
    if certificate_id not in birth_certificates:
        raise HTTPException(status_code=404, detail=f"Certificate ID '{certificate_id}' not found")
    deleted = birth_certificates.pop(certificate_id)
    return {"message": "Certificate deleted", "data": deleted}
