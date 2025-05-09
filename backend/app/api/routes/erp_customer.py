from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app import erp_schemas, erp_crud
from ...api.deps import get_db
from uuid import UUID

router = APIRouter(prefix="/erp/customer", tags=["ERP Customer"])

@router.post("/", response_model=erp_schemas.Customer)
def create_customer(customer: erp_schemas.CustomerCreate, db: Session = Depends(get_db)):
    return erp_crud.create_customer(session=db, customer=customer)

@router.get("/", response_model=list[erp_schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    return db.query(erp_crud.model1.Customer).all()

@router.get("/{customer_id}", response_model=erp_schemas.Customer)
def get_customer(customer_id: UUID, db: Session = Depends(get_db)):
    customer = db.query(erp_crud.model1.Customer).filter_by(id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=erp_schemas.Customer)
def update_customer(customer_id: UUID, customer: erp_schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(erp_crud.model1.Customer).filter_by(id=customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: UUID, db: Session = Depends(get_db)):
    db_customer = db.query(erp_crud.model1.Customer).filter_by(id=customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"detail": "Customer deleted"}