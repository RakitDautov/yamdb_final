from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='Наименование категории',
                            max_length=200)
    slug = models.SlugField(verbose_name='URL-адрес', max_length=50,
                            unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Наименование жанра', max_length=200)
    slug = models.SlugField(verbose_name='URL-адрес', max_length=50,
                            unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Наименование произведения',
                            max_length=100, db_index=True)

    year = models.IntegerField(verbose_name='Год выпуска',
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(dt.now().year)])
    description = models.CharField(verbose_name='Описание',
                                   max_length=200,
                                   blank=True, null=True)
    genre = models.ManyToManyField(to='Genre', verbose_name='Жанр',
                                   related_name='titles')
    category = models.ForeignKey(to='Category', verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True,
                                 related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, verbose_name='Произведение',
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.SmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(10)], verbose_name='Оценка')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-id']

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review, verbose_name='Отзыв',
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-id']

    def __str__(self):
        return self.text
