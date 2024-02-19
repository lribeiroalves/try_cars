from .database import db
from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableList
from typing import Optional, List
import datetime


class RolesUsers(db.Model):
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    permissions:Mapped[MutableList] = mapped_column(MutableList.as_mutable(AsaList()), nullable=True)

    users:Mapped[List['User']] = relationship(secondary='roles_users', back_populates='roles')

    def __repr__(self) -> str:
        return f'Role(id={self.id}, name={self.name}, permissions={self.permissions})'


class User(db.Model, UserMixin):
    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username:Mapped[Optional[str]] = mapped_column(String(64), unique=True)
    password:Mapped[str] = mapped_column(String(255), nullable=False)
    last_login_at:Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))
    current_login_at:Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))
    last_login_ip:Mapped[Optional[str]]
    current_login_ip:Mapped[Optional[str]]
    login_count:Mapped[Optional[int]]
    active:Mapped[bool] = mapped_column(Boolean())
    fs_uniquifier:Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    confirmed_at:Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))

    roles:Mapped['Role'] = relationship(secondary='roles_users', back_populates='users')

    def __repr__(self) -> str:
        return f'User(id={self.id}, email={self.email}, username={self.username})'