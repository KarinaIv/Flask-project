
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class likes(SqlAlchemyBase):
    __tablename__ = 'cart'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    id_products = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    # cnt = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    # cart_or_likes = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    products = orm.relation('products')

