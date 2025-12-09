""" Указывать тут все импорты для корректной работы create_all И drop_all """
import random
from datetime import date, timedelta

from sqlalchemy import Integer, and_, cast, func, select, update

from app.database import BaseOrm, engine, session_factory
from app.users.dao import UserDAO, UserModel


def create_user():
    UserDAO.create(
        username='Spongebob',
        password='acuna_matata',
        fullname='Spongebob Squarepants',
        email='qwerty@gmail.com',
        disabled=False,
        telegram_id=670076879
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.create_all)


async def drop_and_create_database():
    print(BaseOrm.metadata.tables.keys())
    print('='*100)
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
    await create_tables()



def some_sql():
    # create_user()
    # update_sales_report()
    # select_sales_report()
    # select_sales_reports_with_avg()
    

    return 'OK'

