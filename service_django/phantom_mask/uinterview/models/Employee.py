from django.db import models, connection
from django.db.models import Case, When, Value

from uinterview import utils
from uinterview.colors import colors
from uinterview.models.EmployeeBonus import EmployeeBonus


class Employee(models.Model):
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employee'

    name = models.CharField(verbose_name='Name',
                            max_length=255, )

    sex = models.CharField(verbose_name='Sex',
                           max_length=2, )

    sex2 = models.CharField(verbose_name='Sex2',
                            max_length=2,
                            null=True, )

    def __str__(self):
        return f'{self.name}({self.sex})'

    @classmethod
    def insert_test_data(cls):
        rows = [
            ('John', 'M'),
            ('Dan', 'F', 500),
            ('Brad', 'M'),
            ('Tomas', 'F', 2000),
        ]

        EmployeeBonus.objects.all().delete()
        cls.objects.all().delete()

        for row in rows:
            employee = cls(name=row[0],
                           sex=row[1])
            employee.save()
            print(f'inserted employee: {employee}')

            if len(row) == 3:
                employee_bonus = EmployeeBonus()
                employee_bonus.employee = employee
                employee_bonus.bonus = row[2]
                employee_bonus.save()
                print(f'inserted  employee: {employee}, bonus:{employee_bonus.bonus}')

        print(f'insert_employee_test_data done, total: {cls.objects.all().count()}')

    @classmethod
    def clear_sex2(cls):
        cls.objects.all().update(sex2=None)

    @classmethod
    def test_case_1(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Employee test_case_1")
        cls.clear_sex2()
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(EmployeeBonus.objects.all())
        print("""
## Question：
找出表格中員工的獎金小於750元或沒有領到獎金的員工姓名和獎金。
        """.strip())

        print("\n## Answer:")
        gte_750_bonus_employee_ids = EmployeeBonus.objects.filter(bonus__gte=750).values_list('employee_id', flat=True)
        queryset = Employee.objects.exclude(id__in=gte_750_bonus_employee_ids)
        for employee in queryset:
            print(f'name: {employee.name}, bonus: {[int(item.bonus) for item in employee.bonus.all()]}')

    @classmethod
    def test_case_1_2(cls, color=colors.fg.blue):

        print(color)
        print("**********************************************************************************")
        print("# Employee test_case_1_2")
        cls.clear_sex2()
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(EmployeeBonus.objects.all())
        print("""
    ## Question：
    找出表格中員工的獎金小於750元或沒有領到獎金的員工姓名和獎金。
            """.strip())

        print("\n## Answer:")
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT U0.id, 
                           U0.name, 
                           U0.sex, 
                           COALESCE(
                                (SELECT SUM(U2.bonus) 
                                 FROM uinterview_employeebonus U2
                                 WHERE U2.employee_id = U0.id), 0) AS bonus
                    FROM uinterview_employee U0
                    WHERE NOT (U0.id IN (
                                    SELECT U1.employee_id 
                                    FROM uinterview_employeebonus U1 
                                    WHERE U1.bonus >= 750))
                    ORDER BY bonus, U0.name
                """
            )

            utils.print_cursor(cursor)

    @classmethod
    def test_case_2(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Employee test_case_2")
        cls.clear_sex2()
        utils.print_queryset(cls.objects.all())
        print("""
## Question：
員工表格中性別輸入錯誤，請寫一條SQL更新語法，將表格中sex為'M'資料更新為'F'，sex為'F'資料更新為'M'。
                """.strip())

        print("\n## Answer:")
        print("sex2為題目答案。")
        Employee.objects.all().update(
            sex2=Case(
                When(sex='M', then=Value('F')),
                default=Value('M')
            )
        )

        utils.print_queryset(cls.objects.all())

    @classmethod
    def test_case_2_2(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Employee test_case_2_2")
        cls.clear_sex2()
        utils.print_queryset(cls.objects.all())
        print("""
## Question：
員工表格中性別輸入錯誤，請寫一條SQL更新語法，將表格中sex為'M'資料更新為'F'，sex為'F'資料更新為'M'。
                """.strip())

        print("\n## Answer:")
        print("sex2為題目答案。")
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                   UPDATE uinterview_employee 
                   SET sex2 = CASE 
                                WHEN (sex = 'M') THEN 'F' 
                                ELSE 'M' 
                              END
                   RETURNING *;

                """
            )

            utils.print_cursor(cursor)