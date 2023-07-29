from uuid import UUID

from pydantic import BaseModel


class MenuSchemaBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuSchemaOut(MenuSchemaBase):
    id: UUID
    submenus_count: int
    dishes_count: int


class SubmenuSchemaOut(MenuSchemaBase):
    id: UUID
    dishes_count: int


class DishSchemaBase(MenuSchemaBase):
    price: str


class DishSchemaOut(DishSchemaBase):
    id: UUID
