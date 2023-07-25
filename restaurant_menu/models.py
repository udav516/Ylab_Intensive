import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)
    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    dishes_count = Column(Integer, default=0)
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(Float)
    submenu = relationship("Submenu", back_populates="dishes")
