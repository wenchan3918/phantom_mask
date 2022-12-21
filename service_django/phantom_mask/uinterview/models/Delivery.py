from django.db import models, connection
from django.db.models import Count, F, FloatField
from django.db.models.functions import Cast

from uinterview import utils
from uinterview.mixins.ModelFunc import Round
from uinterview.models import Delivery


class Delivery(models.Model):
    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Delivery'

    customer_id = models.IntegerField(verbose_name='Customer ID')

    order_date = models.DateField(
        verbose_name="Order Date",
    )

    delivery_date = models.DateField(
        verbose_name="Delivery Date",
    )

    @classmethod
    def insert_test_data(cls):
        rows = [
            (1, '2019-8-1', '2019-8-2'),
            (5, '2019-8-2', '2019-8-2'),
            (1, '2019-8-11', '2019-8-11'),
            (3, '2019-8-24', '2019-8-26'),
            (4, '2019-8-21', '2019-8-22'),
            (2, '2019-8-11', '2019-8-13'),
        ]

        cls.objects.all().delete()

        for row in rows:
            delivery = Delivery()
            delivery.customer_id = row[0]
            delivery.order_date = row[1]
            delivery.delivery_date = row[2]
            delivery.save()
            print(
                f'inserted customer_id: {delivery.customer_id}, order_date: {delivery.order_date},delivery_date: {delivery.delivery_date}')

        print(f'insert_delivery_test_data done, total: {cls.objects.all().count()}')

    @classmethod
    def test_case_1(cls, color):
        print(color)
        print("**********************************************************************************")
        print("# Delivery test_case_1")
        utils.print_queryset(cls.objects.all())
        print("""
## Question：
如果客户的deliver_date和order_date相同，則該訂單為real-time order，
否則都為plan order查詢表格中real-time order所佔的百分比，四捨五入到小數點後2位。
        """.strip())

        print("\n## Answer:")

        real_order_count = Delivery.objects \
            .filter(delivery_date=F('order_date')) \
            .count()
        queryset = Delivery.objects.aggregate(
            real_time_order_percent=Cast(
                Round(real_order_count * 100.0 / Count('*')),
                FloatField()
            )
        )

        print(queryset)

    @classmethod
    def test_case_1_2(cls, color):
        print(color)
        print("**********************************************************************************")
        print("# Delivery test_case_1_2")
        utils.print_queryset(cls.objects.all())
        print("""
## Question：
如果客户的deliver_date和order_date相同，則該訂單為real-time order，
否則都為plan order查詢表格中real-time order所佔的百分比，四捨五入到小數點後2位。
        """.strip())

        print("\n## Answer:")

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
            SELECT CAST(
                        ROUND(
                            (SELECT COUNT(*) 
                            FROM uinterview_delivery
                            -- 需*100.0，否則會被當成int
                            WHERE uinterview_delivery.delivery_date = uinterview_delivery.order_date) * 100.0  / COUNT(*)
                        , 2) AS double precision) AS real_time_order_percent
            FROM uinterview_delivery
                """
            )

            utils.print_cursor(cursor)

