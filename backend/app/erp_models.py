import uuid
import enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# --- Enums ---

class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class ModuleNameEnum(str, enum.Enum):
    module1 = "module1"
    module2 = "module2"


# --- Models ---

class Address(SQLModel, table=True):
    __tablename__ = "address"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    address_line1: str
    address_line2: Optional[str] = None

    customers: List["Customer"] = Relationship(back_populates="address")


class Customer(SQLModel, table=True):
    __tablename__ = "customer"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    industry: str
    address_id: Optional[uuid.UUID] = Field(default=None, foreign_key="address.id")
    phone_no: str

    address: Optional["Address"] = Relationship(back_populates="customers")
    customer_modules: List["CustomerModule"] = Relationship(back_populates="customer")
    orders: List["Order"] = Relationship(back_populates="customer")


class Module(SQLModel, table=True):
    __tablename__ = "modules"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str

    customer_modules: List["CustomerModule"] = Relationship(back_populates="module")


class CustomerModule(SQLModel, table=True):
    __tablename__ = "customer_module"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(foreign_key="customer.id")
    module_id: uuid.UUID = Field(foreign_key="modules.id")

    customer: "Customer" = Relationship(back_populates="customer_modules")
    module: "Module" = Relationship(back_populates="customer_modules")


class Order(SQLModel, table=True):
    __tablename__ = "order"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(foreign_key="customer.id")
    order_status: Optional[OrderStatusEnum] = None
    amount: float
    erp_username: str
    erp_password: str
    erp_link: str
    company_description: Optional[str] = None

    customer: "Customer" = Relationship(back_populates="orders")
