from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ... import erp_schemas, erp_crud
from ...api.deps import get_db
from uuid import UUID

router = APIRouter(prefix="/erp/order", tags=["ERP Order"])

@router.post("/", response_model=erp_schemas.Order)
def create_order(order: erp_schemas.OrderCreate, db: Session = Depends(get_db)):
    return erp_crud.create_order(session=db, order=order)

@router.get("/", response_model=list[erp_schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    return db.query(erp_crud.model1.Order).all()

@router.get("/{order_id}", response_model=erp_schemas.Order)
def get_order(order_id: UUID, db: Session = Depends(get_db)):
    order = db.query(erp_crud.model1.Order).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=erp_schemas.Order)
def update_order(order_id: UUID, order: erp_schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(erp_crud.model1.Order).filter_by(id=order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.dict().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}")
def delete_order(order_id: UUID, db: Session = Depends(get_db)):
    db_order = db.query(erp_crud.model1.Order).filter_by(id=order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"detail": "Order deleted"}