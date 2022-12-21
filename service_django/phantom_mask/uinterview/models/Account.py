from django.db import connection
from django.db import models

from uinterview import utils
from uinterview.colors import colors
from uinterview.models.AccountLogin import AccountLogin


class Account(models.Model):
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'

    name = models.CharField(verbose_name='Name',
                            max_length=255, )

    def __str__(self):
        return self.name

    @classmethod
    def insert_test_data(cls):
        AccountLogin.objects.all().delete()
        Account.objects.all().delete()

        accounts = [
            (1, 'Wick'),
            (7, 'Jonathan'),

        ]

        for account in accounts:
            obj = Account(
                id=account[0],
                name=account[1])
            obj.save()
            print(f'inserted account: {obj}')

        login_rows = [
            (2, 7, '2020-05-30'),
            (3, 1, '2020-05-30'),
            (4, 7, '2020-05-31'),
            (5, 7, '2020-06-01'),
            (6, 7, '2020-06-02'),
            (7, 7, '2020-06-02'),
            (8, 7, '2020-06-03'),
            (9, 1, '2020-06-07'),
            (10, 7, '2020-06-10'),
        ]

        for login in login_rows:
            obj = AccountLogin(
                id=login[0],
                account=Account.objects.get(id=login[1]),
                login_date=login[2])
            obj.save()
            print(f'inserted account_login: {obj}')

        print(f'insert_account_test_data done, total: {cls.objects.all().count()}')

    @classmethod
    def test_case_1(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Account test_case_1")

        utils.print_queryset(Account.objects.all())
        utils.print_queryset(AccountLogin.objects.all())
        print("""
## Question：
找出表格中連續4天或以上登入的用户帳號的id和名稱，並按id由小到大排序。
(使用OVER 與 PARTITION BY語法來完成)
        """.strip())

        print("\n## Answer:")
        consecutive_login_days = 1
        consecutive_login_days = 4
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT account_id, 
                    (SELECT name FROM uinterview_account WHERE id = account_id) AS name,
                    CONCAT(count(sub_date),'天') AS login_days,
                    first_login_at 
                FROM (
                     SELECT account_id,
                            group_seq,
                            TO_CHAR(login_date,'YYYY-mm-dd') AS login_date,
                            TO_CHAR(sub_date,'YYYY-mm-dd') AS sub_date,
                            TO_CHAR(
                            CASE 
                                 WHEN group_seq = 1 THEN login_date
                                 WHEN sub_date = LAG(sub_date,1) OVER(PARTITION BY account_id ORDER BY login_date) 
                                      THEN LAG(login_date,CAST(group_seq AS INT)-1) OVER()
                                 ELSE login_date 
                                 END
                            ,'YYYY-mm-dd') AS first_login_at
                     FROM (
                            --如有連續相同sub_date代表是連續登入日期
                            --例如:
                            --  login_date(2022-01-02) - group_seq(1) = 2022-01-01
                            --  login_date(2022-01-03) - group_seq(2) = 2022-01-01
                            --  login_date(2022-01-04) - group_seq(3) = 2022-01-01
                            --  login_date(2022-01-10) - group_seq(4) = 2022-01-06
                            SELECT *,
                                   login_date - (group_seq || 'DAY')::INTERVAL AS sub_date
                            FROM(
                                -- 以group_seq來分組，後續login_date - group_seq天來判斷是否為連續登入
                                SELECT *, 
                                       ROW_NUMBER() OVER(PARTITION BY account_id ORDER BY login_date) AS group_seq
                                FROM (
                                        -- 過濾掉同一天多次登入日期，只保留一筆資料
                                        SELECT DISTINCT account_id ,login_date
                                        FROM uinterview_accountlogin
                                        ORDER BY login_date
                                ) U0
                            ) U1
                     ) U2
                ) U3 
                GROUP BY account_id,sub_date,first_login_at  
                HAVING count(*) >= {consecutive_login_days}
                ORDER BY account_id,first_login_at;
                """
            )

            utils.print_cursor(cursor)
