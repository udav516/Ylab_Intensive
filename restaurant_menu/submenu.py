from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from database import get_db
from models import Menu, Submenu
from schemas import MenuSchemaBase, SubmenuSchemaOut

router = APIRouter()


@router.get("/")
def get(db: Session = Depends(get_db)) -> list[SubmenuSchemaOut]:
    _submenu = db.query(Submenu).all()
    return _submenu


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
        menu_id: UUID, submenu: MenuSchemaBase, db: Session = Depends(get_db)
) -> SubmenuSchemaOut:
    _submenu = Submenu(**submenu.dict())
    _submenu.menu_id = menu_id
    db.add(_submenu)
    db.commit()
    db.refresh(_submenu)
    _menu = db.query(Menu).filter(Menu.id == _submenu.menu_id).first()
    _menu.submenus_count += 1
    db.commit()
    db.refresh(_menu)
    return _submenu


@router.get("/{id}")
def get_by_id(id: UUID, db: Session = Depends(get_db)) -> SubmenuSchemaOut:
    _submenu = db.query(Submenu).filter(Submenu.id == id).first()
    if not _submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return _submenu


@router.patch("/{id}")
def update(
        id: UUID, submenu: MenuSchemaBase, db: Session = Depends(get_db)
) -> SubmenuSchemaOut:
    _submenu = db.query(Submenu).filter(Submenu.id == id)
    db_submenu = _submenu.first()
    if not _submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    _submenu.update(submenu.dict(exclude_unset=True))
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


@router.delete("/{id}")
def delete(id: UUID, db: Session = Depends(get_db)) -> Dict:
    _submenu = db.query(Submenu).filter(Submenu.id == id).first()
    db.delete(_submenu)
    db.commit()
    _menu = db.query(Menu).filter(Menu.id == _submenu.menu_id).first()
    _menu.submenus_count -= 1
    _menu.dishes_count -= _submenu.dishes_count
    db.commit()
    db.refresh(_menu)
    return {"status": True, "message": "The submenu has been deleted"}
