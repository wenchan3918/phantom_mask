from django.db import models, connection

from uinterview import utils
from uinterview.colors import colors


class Email(models.Model):
    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Email'

    email = models.CharField(verbose_name='Email',
                             max_length=128, )

    is_delete = models.BooleanField(verbose_name='is Delete',
                                    default=False,
                                    blank=True,
                                    null=True, )

    @classmethod
    def insert_test_data(cls):
        rows = [
            'alan@gexample.com',
            'bob@gexample.com',
            'alan@gexample.com',
        ]

        cls.objects.all().delete()

        for email in rows:
            cls(email=email).save()
            print(
                f'inserted email: {email}')

        print(f'insert_email_test_data done, total: {cls.objects.all().count()}')

    @classmethod
    def reset_delete_email(cls):
        cls.objects.filter(is_delete=True).update(is_delete=False)

    def __str__(self):
        return self.email

    @classmethod
    def test_case_1(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Email test_case_1")
        cls.reset_delete_email()
        utils.print_queryset(cls.objects.all())
        print("""
## Question：
删除表格中有重複email的資料，當資料中有重複的email時，保留Id最小的資料。
        """.strip())

        print("\n## Answer:")

        keep_email_ids = Email.objects.values_list('id', flat=True) \
            .distinct('email') \
            .order_by('email', 'id')

        Email.objects.exclude(id__in=keep_email_ids).update(is_delete=True)

        utils.print_queryset(cls.objects.all().order_by('id'))

    @classmethod
    def test_case_1_2(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Email test_case_1_2")
        cls.reset_delete_email()
        utils.print_queryset(cls.objects.all())
        print("""
## Question：
删除表格中有重複email的資料，當資料中有重複的email時，保留Id最小的資料。
        """.strip())

        print("\n## Answer:")

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                 UPDATE uinterview_email
                 SET is_delete = true 
                 WHERE NOT (id IN (
                                SELECT DISTINCT ON (email) id 
                                FROM uinterview_email 
                                ORDER BY email ASC, id ASC)
                          )
                 RETURNING *;
                """
            )

            utils.print_cursor(cursor)
