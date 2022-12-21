from django.db import models


class MovieRating(models.Model):
    class Meta:
        verbose_name = 'Movie Rating'
        verbose_name_plural = 'Movie Rating'

    movie = models.ForeignKey('Movie',
                              verbose_name='Movie',
                              related_name='movie',
                              on_delete=models.CASCADE,
                              )

    user = models.ForeignKey('User',
                             verbose_name='User',
                             related_name='user',
                             on_delete=models.CASCADE,
                             )

    rating = models.SmallIntegerField(verbose_name='Rating',
                                      default=0,
                                      db_index=True, )

    create_date = models.DateField(verbose_name='Create Date', )
