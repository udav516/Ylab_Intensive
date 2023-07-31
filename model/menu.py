from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from controller.database import get_db
from controller.models import Menu
from controller.schemas import MenuSchemaOut, MenuSchemaBase

router = APIRouter()


@router.get("/")
def get(db: Session = Depends(get_db)) -> List[MenuSchemaOut]:
    _menu = db.query(Menu).all()
    return _menu


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
        menu: MenuSchemaBase, db: Session = Depends(get_db)
) -> MenuSchemaOut:
    _menu = Menu(**menu.dict())
    db.add(_menu)
    db.commit()
    db.refresh(_menu)
    return _menu


@router.get("/{id}")
def get_by_id(id: UUID, db: Session = Depends(get_db)) -> MenuSchemaOut:
    _menu = db.query(Menu).filter(Menu.id == id).first()
    if not _menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return _menu


@router.patch("/{id}")
def update(
        id: UUID, menu: MenuSchemaBase, db: Session = Depends(get_db)
) -> MenuSchemaOut:
    _menu = db.query(Menu).filter(Menu.id == id)
    db_menu = _menu.first()
    if not _menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    _menu.update(menu.dict(exclude_unset=True))
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.delete("/{id}")
def delete(id: UUID, db: Session = Depends(get_db)) -> Dict:
    _menu = db.query(Menu).filter(Menu.id == id).first()
    db.delete(_menu)
    db.commit()
    return {"status": True, "message": "The menu has been deleted"}
