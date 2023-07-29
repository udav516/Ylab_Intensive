import uvicorn
from fastapi import FastAPI

from restaurant_menu.model import dish, menu, submenu

app = FastAPI(title="Restaurant menus")

app.include_router(menu.router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(
    submenu.router,
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["submenus"],
)
app.include_router(
    dish.router,
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["dishes"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
