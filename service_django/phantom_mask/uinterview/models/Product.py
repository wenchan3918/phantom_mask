from datetime import datetime, timedelta

from django.db import models, connection
from django.db.models import Subquery, OuterRef, Func
from django.db.models.functions import Coalesce

from uinterview import utils
from uinterview.colors import colors
from uinterview.models.Order import Order


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product"

    name = models.CharField(verbose_name='Name',
                            max_length=256, )

    available_date = models.DateTimeField(verbose_name='Available Date')

    def __str__(self):
        return self.name

    @classmethod
    def insert_test_data(cls):
        rows = [
            (1, 'Product1', '2010-01-01 00:00:00', [
                (1, 4, '2018-07-26 00:00:00'),
                (2, 2, '2018-11-05 00:00:00'),
            ]),
            (2, 'Product2', '2012-05-12 00:00:00', [

            ]),
            (3, 'Product3', '2019-06-10 00:00:00', [
                (3, 1, '2019-06-11 00:00:00'),
            ]),
            (4, 'Product4', '2019-06-01 00:00:00', [
                (4, 8, '2019-06-05 00:00:00'),
                (5, 6, '2019-06-20 00:00:00'),
            ]),
            (5, 'Product5', '2008-09-21 00:00:00', [
                (6, 5, '2009-02-02 00:00:00'),
                (7, 9, '2010-04-13 00:00:00'),
            ]),

        ]

        Order.objects.all().delete()
        cls.objects.all().delete()

        for row in rows:
            product = cls(id=row[0],
                          name=row[1],
                          available_date=row[2])
            product.save()
            print(f'inserted product: {product.name}, available_date: {product.available_date}')

            for row2 in row[3]:
                order = Order(id=row2[0],
                              product=product,
                              qty=row2[1],
                              dispatch_date=row2[2])

                order.save()
                print(f'   inserted  order, quantity: {order.qty}, dispatch_date: {order.dispatch_date}')

        print(f'insert_product_test_data done, total: {cls.objects.all().count()}')

    @classmethod
    def test_case_1(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Product test_case_1")
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(Order.objects.all())
        print("""
## Question：
假設今天是2019-6-23，找出表格中找出過去一年内銷售數量少於10的產品id和名稱，並排除available_date小於一個月的產品。
        """.strip())

        print("\n## Answer:")
        now = datetime.strptime("2019-6-23", "%Y-%m-%d")

        order_queryset = Order.objects \
            .filter(product=OuterRef('pk')) \
            .filter(dispatch_date__gte=now - timedelta(days=365)) \
            .annotate(total_of_qty=Coalesce(Func('qty', function='Sum'), 0)) \
            .values('total_of_qty')

        queryset = Product.objects \
            .annotate(total_of_qty=Subquery(order_queryset)) \
            .filter(total_of_qty__lt=10) \
            .filter(available_date__gte=now - timedelta(days=30))

        utils.print_queryset(queryset, ['total_of_qty'])

        # for p in queryset:
        #     print(f'id:{p.id}, 名稱: {p.name}, 總銷售數量: {p.total_of_qty}, 有效日期: {p.available_date}')

    @classmethod
    def test_case_1_2(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Product test_case_1_2")
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(Order.objects.all())
        print("""
## Question：
假設今天是2019-6-23，找出表格中找出過去一年内銷售數量少於10的產品id和名稱，並排除available_date小於一個月的產品。
        """.strip())

        print("\n## Answer:")
        now = datetime.strptime("2019-6-23", "%Y-%m-%d")

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT id, 
                           name, 
                           available_date, 
                           (SELECT COALESCE(Sum(U1.qty), 0) 
                            FROM uinterview_order U1 
                            WHERE (U1.product_id = U0.id 
                                  AND dispatch_date >= '2018-06-23T00:00:00'::timestamp)) AS total_of_qty 
                    FROM uinterview_product U0
                    WHERE ((SELECT COALESCE(Sum(U2.qty), 0) 
                            FROM uinterview_order U2
                            WHERE (U2.product_id = U0.id AND U2.dispatch_date >= '2018-06-23T00:00:00'::timestamp)) < 10 
                            
                            AND U0.available_date >= '2019-05-24T00:00:00'::timestamp) 

                """
            )

            utils.print_cursor(cursor)
