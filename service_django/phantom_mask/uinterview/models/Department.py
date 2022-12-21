from django.db import models, connection
from django.db.models import OuterRef, Func, Count, Subquery
from django.db.models.functions import Coalesce

from uinterview import utils
from uinterview.colors import colors
from uinterview.models import Student
from uinterview.models.EmployeeBonus import EmployeeBonus


class Department(models.Model):
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Department'

    name = models.CharField(verbose_name='Name',
                            max_length=255, )

    def __str__(self):
        return self.name

    @classmethod
    def insert_test_data(cls):
        rows = [
            (1, 'Engineering', [
                (1, 'Jack', 'M'),
                (2, 'Jan', 'F'),
            ]),
            (2, 'Science', [
                (3, 'Mark', 'M'),
            ]),
            (3, 'Law', [

            ]),
        ]

        Student.objects.all().delete()
        cls.objects.all().delete()

        for row in rows:
            department = cls(
                id=row[0],
                name=row[1])
            department.save()
            print(f'inserted department: {department}')

            for row2 in row[2]:
                student = Student(
                    id=row2[0],
                    department=department,
                    name=row2[1],
                    gender=row2[2]
                )
                student.save()
                print(f'    inserted student: {student}')

        print(f'insert_department_test_data done, total: {cls.objects.all().count()}')

    @classmethod
    def test_case_1(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Department test_case_1")
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(Student.objects.all())
        print("""
## Question：
找出表格中所有部門的學生人數，並按學生人數由大到小、部門名稱由小到大排序。
        """.strip())

        print("\n## Answer:")
        student_queryset = Student.objects \
            .filter(department=OuterRef('pk')) \
            .annotate(total_of_students=Coalesce(Func('id', function='Count'), 0)) \
            .values('total_of_students')

        department_queryset = Department.objects \
            .annotate(total_of_students=Subquery(student_queryset)) \
            .order_by('-total_of_students', 'name')

        utils.print_queryset(department_queryset, ['total_of_students'])
        # for department in department_queryset:
        #     department_name = str(department.name).ljust(12, " ")
        #     department_total_of_students = str(department.total_of_students).rjust(2, " ")
        #     print(f'人數: {department_total_of_students}, 部門: {department_name}')

    @classmethod
    def test_case_1_2(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Department test_case_1_2")
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(Student.objects.all())
        print("""
## Question：
找出表格中所有部門的學生人數，並按學生人數由大到小、部門名稱由小到大排序。
        """.strip())

        print("\n## Answer:")
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT id, 
                           name, 
                           (SELECT COALESCE(Count(*), 0)
                            FROM uinterview_student U1
                            WHERE U1.department_id = U0.id) AS total_of_students 
                    FROM uinterview_department U0 
                    ORDER BY total_of_students DESC, name ASC;
                   """
            )

            utils.print_cursor(cursor)
