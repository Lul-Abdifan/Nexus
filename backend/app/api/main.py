from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils
from app.core.config import settings
from app.api.routes import erp_address, erp_customer, erp_module, erp_order, erp_customer_module



api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)

api_router.include_router(erp_address.router)
api_router.include_router(erp_customer.router)
api_router.include_router(erp_module.router)
api_router.include_router(erp_order.router)
api_router.include_router(erp_customer_module.router)
if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
