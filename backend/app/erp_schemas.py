from pydantic import BaseModel, UUID4
from typing import Optional
import enum
import uuid

class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class ModuleNameEnum(str, enum.Enum):
    module1 = "module1"
    module2 = "module2"

class AddressBase(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: UUID4
    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    industry: str
    address_id: uuid.UUID  # ✅ Rename this field to match your model
    phone_no: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: UUID4
    class Config:
        orm_mode = True

# class ModuleBase(BaseModel):
#     name: ModuleNameEnum

class ModuleBase(BaseModel):
    name: str  # ✅ Accept any module name dynamically

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    id: UUID4
    class Config:
        orm_mode = True

class CustomerModuleBase(BaseModel):
    customer_id: UUID4
    module_id: UUID4

class CustomerModuleCreate(CustomerModuleBase):
    pass

class CustomerModule(CustomerModuleBase):
    id: UUID4
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_id: UUID4
    order_status: Optional[OrderStatusEnum] = None
    amount: float
    erp_username: str
    erp_password: str
    erp_link: str
    company_description: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: UUID4
    class Config:
        orm_mode = True