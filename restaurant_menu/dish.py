from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from database import get_db
from models import Dish, Menu, Submenu
from schemas import DishSchemaBase, DishSchemaOut

router = APIRouter()


@router.get("/")
async def get(db: Session = Depends(get_db)) -> List[DishSchemaOut]:
    _dish = db.query(Dish).all()
    return _dish


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
        submenu_id: UUID, dish: DishSchemaBase, db: Session = Depends(get_db)
) -> DishSchemaOut:
    _dish = Dish(**dish.dict())
    _dish.submenu_id = submenu_id
    db.add(_dish)
    db.commit()
    db.refresh(_dish)
    _submenu = db.query(Submenu).filter(Submenu.id == _dish.submenu_id).first()
    _submenu.dishes_count += 1
    db.commit()
    db.refresh(_submenu)
    _menu = db.query(Menu).filter(Menu.id == _submenu.menu_id).first()
    _menu.dishes_count += 1
    db.commit()
    db.refresh(_menu)
    return _dish


@router.get("/{id}")
def get_by_id(id: UUID, db: Session = Depends(get_db)) -> DishSchemaOut:
    _dish = db.query(Dish).filter(Dish.id == id).first()
    if not _dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return _dish


@router.patch("/{id}")
def update(
        id: UUID, dish: DishSchemaBase, db: Session = Depends(get_db)
) -> DishSchemaOut:
    _dish = db.query(Dish).filter(Dish.id == id)
    db_dish = _dish.first()
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    _dish.update(dish.dict(exclude_unset=True))
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.delete("/{id}")
def delete(id: UUID, db: Session = Depends(get_db)) -> Dict:
    _dish = db.query(Dish).filter(Dish.id == id).first()
    if _dish:
        _submenu = _dish.submenu
        _menu = _submenu.menu
        db.delete(_dish)
        db.commit()
        db.refresh(_submenu)
        db.refresh(_menu)
        return {"status": True, "message": "The dish has been deleted"}
    else:
        return {"status": False, "message": "Dish not found"}
