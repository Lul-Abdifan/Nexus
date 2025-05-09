from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ... import erp_schemas, erp_crud
from ...api.deps import get_db
from uuid import UUID

router = APIRouter(prefix="/erp/module", tags=["ERP Module"])

@router.post("/", response_model=erp_schemas.Module)
def create_module(module: erp_schemas.ModuleCreate, db: Session = Depends(get_db)):
    return erp_crud.create_module(session=db, module=module)

@router.get("/", response_model=list[erp_schemas.Module])
def list_modules(db: Session = Depends(get_db)):
    return db.query(erp_crud.model1.Module).all()

@router.get("/{module_id}", response_model=erp_schemas.Module)
def get_module(module_id: UUID, db: Session = Depends(get_db)):
    module = db.query(erp_crud.model1.Module).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@router.put("/{module_id}", response_model=erp_schemas.Module)
def update_module(module_id: UUID, module: erp_schemas.ModuleCreate, db: Session = Depends(get_db)):
    db_module = db.query(erp_crud.model1.Module).filter_by(id=module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    for key, value in module.dict().items():
        setattr(db_module, key, value)
    db.commit()
    db.refresh(db_module)
    return db_module

@router.delete("/{module_id}")
def delete_module(module_id: UUID, db: Session = Depends(get_db)):
    db_module = db.query(erp_crud.model1.Module).filter_by(id=module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    db.delete(db_module)
    db.commit()
    return {"detail": "Module deleted"}