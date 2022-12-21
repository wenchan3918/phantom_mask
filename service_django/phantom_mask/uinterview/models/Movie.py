from django.db import models, connection
from django.db.models import OuterRef, Func, Subquery, Max, When, F, Case, BooleanField
from django.db.models.functions import Coalesce

from uinterview import utils
from uinterview.colors import colors
from uinterview.models.User import User
from uinterview.models.MovieRating import MovieRating


class Movie(models.Model):
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movie'

    name = models.CharField(verbose_name='Name',
                            max_length=255, )

    def __str__(self):
        return self.name

    @classmethod
    def insert_test_data(cls):
        MovieRating.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()

        movies = [
            (1, 'Avengers'),
            (2, 'Frozen 2'),
            (3, 'Joker'),
        ]

        for movie in movies:
            obj = Movie(
                id=movie[0],
                name=movie[1])
            obj.save()
            print(f'inserted movie: {obj}')

        users = [
            (1, 'Daniel'),
            (2, 'Monica'),
            (3, 'Maria'),
            (4, 'James'),
        ]

        for user in users:
            obj = User(
                id=user[0],
                name=user[1])
            obj.save()
            print(f'inserted user: {obj}')

        ratings = [
            (1, 1, 1, 3, '2020-01-12'),
            (2, 1, 2, 4, '2020-02-11'),
            (3, 1, 3, 2, '2020-02-12'),
            (4, 1, 4, 1, '2020-01-01'),
            (5, 2, 1, 5, '2020-02-17'),
            (6, 2, 2, 2, '2020-02-01'),
            (7, 2, 3, 2, '2020-03-01'),
            (8, 3, 1, 3, '2020-02-22'),
            (9, 3, 2, 4, '2020-02-25'),
        ]

        for rating in ratings:
            obj = MovieRating(
                id=rating[0],
                movie=Movie.objects.get(id=rating[1]),
                user=User.objects.get(id=rating[2]),
                rating=rating[3],
                create_date=rating[4])
            obj.save()
            print(
                f'inserted movie_rating: id: {obj.id}, movie_id: {obj.movie.id}, user_id: {obj.user.id}, rating: {obj.rating}, create_date: {obj.create_date}')

        print(f'insert_movie_test_data done, total: {cls.objects.all().count()}')

    @classmethod
    def test_case_1(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Movie test_case_1")
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(User.objects.all())
        utils.print_queryset(MovieRating.objects.all())
        print("""
## Question：
找出表格中評論最多部電影的用戶，如果評論數相同，依用户名稱由小到大排序。
        """.strip())

        print("\n## Answer:")
        movie_comment_queryset = MovieRating.objects \
            .filter(user=OuterRef('pk')) \
            .annotate(total_of_comment=Func('id', function='Count')) \
            .values('total_of_comment')

        user_queryset = User.objects \
            .annotate(total_of_comment=Subquery(movie_comment_queryset)) \
            .order_by('-total_of_comment', 'name')

        user_queryset = user_queryset \
            .annotate(is_most= \
                          Case(When(total_of_comment=user_queryset.first().total_of_comment, then=True), )
                      )

        utils.print_queryset(user_queryset, ['total_of_comment', 'is_most'])

        # for idx, user in enumerate(user_queryset):
        #     user_name = str(user.name).ljust(8, " ")
        #     user_total_of_students = str(user.total_of_comment).rjust(2, " ")
        #     print(f'用戶: {user_name}, 評論數: {user_total_of_students}{"，為評論最多的用戶" if idx == 0 else ""}')

    @classmethod
    def test_case_1_2(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Movie test_case_1_2")
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(User.objects.all())
        utils.print_queryset(MovieRating.objects.all())
        print("""
## Question：
找出表格中評論最多部電影的用戶，如果評論數相同，依用户名稱由小到大排序。
            """.strip())

        print("\n## Answer:")
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                -- 透過GROUP BY user_id後在進行COUNT(*)，可以得到每個user的評論次數
                 SELECT * 
                 FROM (SELECT user_id,
                               (SELECT name FROM uinterview_user WHERE id = user_id) AS user_name,
                               COUNT(*) AS total_of_comment
                       FROM uinterview_movierating
                       GROUP BY user_id
                       ORDER BY total_of_comment DESC, user_name ASC) U0
                 WHERE total_of_comment = ( SELECT MAX(total_of_comment) 
                                            FROM (SELECT user_id,COUNT(*) AS total_of_comment
                                                   FROM uinterview_movierating
                                                   GROUP BY user_id) U1
                                          )
                """
            )

            utils.print_cursor(cursor)

    @classmethod
    def test_case_2(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Movie test_case_2")
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(User.objects.all())
        utils.print_queryset(MovieRating.objects.all())
        print("""
## Question：
並找出2020/2月平均評分最高的電影名稱，如果評分相同，依電影名稱由小到大排序。
        """.strip())

        print("\n## Answer:")
        movie_rating_queryset = MovieRating.objects \
            .filter(movie=OuterRef('pk')) \
            .filter(create_date__year=2020, create_date__month=2) \
            .annotate(total_of_rating=Func('rating', function='Sum')) \
            .values('total_of_rating')

        movie_queryset = Movie.objects \
            .annotate(total_of_rating=Subquery(movie_rating_queryset)) \
            .order_by('-total_of_rating', 'name')

        movie_queryset = movie_queryset \
            .annotate(is_top=Case(
            When(total_of_rating=movie_queryset.first().total_of_rating, then=True),
        )
        )

        utils.print_queryset(movie_queryset, ['total_of_rating', 'is_top'])

    #     for idx, movie in enumerate(movie_queryset):
    #         movie_name = str(movie.name).ljust(10, " ")
    #         movie_total_of_rating = str(movie.total_of_rating).rjust(2, " ")
    #         print(f'電影: {movie_name}, {movie.max},評分: {movie_total_of_rating}{"，為2020/2月最高評分" if idx == 0 else ""}')
    #
    #
    @classmethod
    def test_case_2_2(cls, color=colors.fg.blue):
        print(color)
        print("**********************************************************************************")
        print("# Movie test_case_2_2")
        utils.print_queryset(cls.objects.all())
        utils.print_queryset(User.objects.all())
        utils.print_queryset(MovieRating.objects.all())
        print("""
## Question：
並找出2020/2月平均評分最高的電影名稱，如果評分相同，依電影名稱由小到大排序。
        """.strip())

        print("\n## Answer:")
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                 -- 透過GROUP BY movie_id後在進行SUM(rating)，可以得到每個movie的評分總和
                 SELECT * 
                 FROM (SELECT movie_id,
                              (SELECT name 
                                FROM uinterview_movie 
                                WHERE id = movie_id) AS movie_name,
                              SUM(rating) AS total_of_rating
                       FROM uinterview_movierating
                       WHERE create_date BETWEEN '2020-02-01' AND '2020-02-29'
                       GROUP BY movie_id
                       ORDER BY total_of_rating DESC, movie_name ASC) U0
                 WHERE total_of_rating = ( SELECT MAX(total_of_rating) 
                                           FROM (SELECT movie_id, SUM(rating) AS total_of_rating
                                                   FROM uinterview_movierating
                                                   WHERE create_date BETWEEN '2020-02-01' AND '2020-02-29'
                                                   GROUP BY movie_id) U1
                                          )

                """
            )

            utils.print_cursor(cursor)
