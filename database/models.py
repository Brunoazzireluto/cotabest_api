from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from sqlalchemy.dialects.mysql import FLOAT

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    price = Column(Float, nullable=False)
    minimun = Column(Integer, nullable=False)
    amount_per_package = Column(Integer, nullable=False)
    max_availability = Column(Integer, nullable=False)


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(String(200), primary_key=True, index=True)
    buyer = Column(Integer, nullable=False, index=True)

    items = relationship('CartItem', back_populates='cart_items')


class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, index=True)
    id_cart = Column(String(200), ForeignKey('carts.id'), index=True)
    id_item = Column(Integer, nullable=False )
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

    cart_items = relationship('Cart', back_populates='items')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(String(200), primary_key=True, index=True)
    buyer = Column(Integer, nullable=False, index=True)

    items = relationship('OrderItem', back_populates='order_items')


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    id_order = Column(String(200), ForeignKey('orders.id'), index=True)
    id_item = Column(Integer, nullable=False )
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)


    order_items = relationship('Order', back_populates='items')

