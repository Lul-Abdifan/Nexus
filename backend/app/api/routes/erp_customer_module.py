from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ... import erp_schemas, erp_crud
from ...api.deps import get_db
from uuid import UUID

router = APIRouter(prefix="/erp/customer_module", tags=["ERP CustomerModule"])

@router.post("/", response_model=erp_schemas.CustomerModule)
def create_customer_module(cm: erp_schemas.CustomerModuleCreate, db: Session = Depends(get_db)):
    return erp_crud.create_customer_module(session=db, cm=cm)

@router.get("/", response_model=list[erp_schemas.CustomerModule])
def list_customer_modules(db: Session = Depends(get_db)):
    return db.query(erp_crud.model1.CustomerModule).all()

@router.get("/{customer_module_id}", response_model=erp_schemas.CustomerModule)
def get_customer_module(customer_module_id: UUID, db: Session = Depends(get_db)):
    cm = db.query(erp_crud.model1.CustomerModule).filter_by(id=customer_module_id).first()
    if not cm:
        raise HTTPException(status_code=404, detail="CustomerModule not found")
    return cm

@router.put("/{customer_module_id}", response_model=erp_schemas.CustomerModule)
def update_customer_module(customer_module_id: UUID, cm: erp_schemas.CustomerModuleCreate, db: Session = Depends(get_db)):
    db_cm = db.query(erp_crud.model1.CustomerModule).filter_by(id=customer_module_id).first()
    if not db_cm:
        raise HTTPException(status_code=404, detail="CustomerModule not found")
    for key, value in cm.dict().items():
        setattr(db_cm, key, value)
    db.commit()
    db.refresh(db_cm)
    return db_cm

@router.delete("/{customer_module_id}")
def delete_customer_module(customer_module_id: UUID, db: Session = Depends(get_db)):
    db_cm = db.query(erp_crud.model1.CustomerModule).filter_by(id=customer_module_id).first()
    if not db_cm:
        raise HTTPException(status_code=404, detail="CustomerModule not found")
    db.delete(db_cm)
    db.commit()
    return {"detail": "CustomerModule deleted"}