from sqlmodel import Session, select
from app import erp_models, erp_schemas

def create_address(*, session: Session, address: erp_schemas.AddressCreate) -> erp_models.Address:
    db_address = erp_models.Address.model_validate(address)
    session.add(db_address)
    session.commit()
    session.refresh(db_address)
    return db_address

def create_customer(*, session: Session, customer: erp_schemas.CustomerCreate) -> erp_models.Customer:
    db_customer = erp_models.Customer.model_validate(customer)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer

def create_module(*, session: Session, module: erp_schemas.ModuleCreate) -> erp_models.Module:
    db_module = erp_models.Module.model_validate(module)
    session.add(db_module)
    session.commit()
    session.refresh(db_module)
    return db_module

def create_customer_module(*, session: Session, cm: erp_schemas.CustomerModuleCreate) -> erp_models.CustomerModule:
    db_cm = erp_models.CustomerModule.model_validate(cm)
    session.add(db_cm)
    session.commit()
    session.refresh(db_cm)
    return db_cm

def create_order(*, session: Session, order: erp_schemas.OrderCreate) -> erp_models.Order:
    db_order = erp_models.Order.model_validate(order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order