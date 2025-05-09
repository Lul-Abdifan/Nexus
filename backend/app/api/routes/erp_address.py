from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ... import erp_schemas, erp_crud
from ...api.deps import get_db
from uuid import UUID

router = APIRouter(prefix="/erp/address", tags=["ERP Address"])

@router.post("/", response_model=erp_schemas.Address)
def create_address(address: erp_schemas.AddressCreate, db: Session = Depends(get_db)):
    return erp_crud.create_address(session=db, address=address)

@router.get("/", response_model=list[erp_schemas.Address])
def list_addresses(db: Session = Depends(get_db)):
    return db.query(erp_crud.model1.Address).all()

@router.get("/{address_id}", response_model=erp_schemas.Address)
def get_address(address_id: UUID, db: Session = Depends(get_db)):
    address = db.query(erp_crud.model1.Address).filter_by(id=address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=erp_schemas.Address)
def update_address(address_id: UUID, address: erp_schemas.AddressCreate, db: Session = Depends(get_db)):
    db_address = db.query(erp_crud.model1.Address).filter_by(id=address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address

@router.delete("/{address_id}")
def delete_address(address_id: UUID, db: Session = Depends(get_db)):
    db_address = db.query(erp_crud.model1.Address).filter_by(id=address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return {"detail": "Address deleted"}