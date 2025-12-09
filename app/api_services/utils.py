""" Указывать тут все импорты для корректной работы create_all И drop_all """
import random
from datetime import date, timedelta

from sqlalchemy import Integer, and_, cast, func, select, update

from app.database import BaseOrm, engine, session_factory
from app.users.dao import UserDAO, UserOrm


def create_user():
    UserDAO.create(
        username='Spongebob',
        password='acuna_matata',
        fullname='Spongebob Squarepants',
        email='qwerty@gmail.com',
        disabled=False,
        telegram_id=670076879
    )


def create_tables():
    BaseOrm.metadata.create_all(engine)


def drop_and_create_database():
    print(BaseOrm.metadata.tables.keys())
    print('='*100)
    BaseOrm.metadata.drop_all(engine)
    create_tables()




def update_sales_report():
    with session_factory() as session:
        query = update(UserOrm).values(
                name=random.choice(['Бобер', 'Цыпа', 'Голубио']),
                fullname=random.choice(['Бобер', 'Цыпа', 'Голубио'])
            ).filter_by(id=2)
        session.execute(query)
        session.commit()


def select_sales_reports_with_avg():
    with session_factory() as session:
        """
        SELECT successful_orders, CAST(avg(cancelled_orders) AS INTEGER) AS avg_cancelled_orders
        FROM sales_report
        WHERE top_product_name LIKE '%Фитнес-браслет%' AND successful_orders > 10
        GROUP BY successful_orders
        """
        query = (
            select(
                SalesReportOrm.successful_orders,
                cast(func.avg(SalesReportOrm.cancelled_orders), Integer).label('avg_cancelled_orders')
            )
            .filter(and_(
                SalesReportOrm.top_product_name.contains('Фитнес-браслет'),
                SalesReportOrm.successful_orders > 10
            ))
            .group_by(SalesReportOrm.successful_orders)
        )

        r = session.execute(query).all()
        print(query.compile(compile_kwargs={'literal_binds': True}))  # вывод SQL с подставленными параметрами
        print(r)  # [(42, 6), (31, 8), (18, 3)]
        print(r[0].avg_cancelled_orders)  # 6  # берем первую запись и обращаемся к label





def some_sql():
    # create_user()
    # update_sales_report()
    # select_sales_report()
    create_sales_reports()
    # select_sales_reports_with_avg()
    

    return 'OK'

