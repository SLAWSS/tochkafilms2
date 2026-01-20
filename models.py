from django.db import models
from django.contrib.auth.models import User


class Actor(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    birth_date = models.DateField(verbose_name="Дата рождения")
    birth_place = models.CharField(max_length=200, verbose_name="Место рождения")
    biography = models.TextField(verbose_name="Биография")
    photo = models.ImageField(upload_to="actors/", verbose_name="Фотография")
    height = models.IntegerField(null=True, blank=True, verbose_name="Рост (см)")
    awards = models.TextField(blank=True, verbose_name="Награды")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def get_films_count(self):
        return self.films.count()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    poster = models.ImageField(upload_to="posters/", verbose_name="Постер")
    trailer_url = models.URLField(blank=True, verbose_name="Трейлер")
    video_file = models.FileField(upload_to="videos/", blank=True, verbose_name="Видео файл")
    year = models.IntegerField(verbose_name="Год выпуска")
    duration = models.IntegerField(verbose_name="Длительность (мин)")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, verbose_name="Рейтинг")
    categories = models.ManyToManyField(Category, related_name="films", verbose_name="Категории")
    actors = models.ManyToManyField(Actor, related_name="films", blank=True, verbose_name="Актеры")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемое")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    favorites = models.ManyToManyField(Film, related_name="favorited_by", blank=True)
    watchlist = models.ManyToManyField(Film, related_name="in_watchlist", blank=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ["film", "user"]

    def __str__(self):
        return f"{self.user.username} - {self.film.title}"


class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="view_history")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="views")
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "История просмотра"
        verbose_name_plural = "История просмотров"
        unique_together = ["user", "film"]
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"{self.user.username} смотрел {self.film.title}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_film', 'Новый фильм'),
        ('new_review', 'Новый отзыв'),
        ('recommendation', 'Рекомендация'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.title}"
