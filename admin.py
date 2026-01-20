from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Film, Actor, UserProfile, Review, ViewHistory, Notification


# Настройка заголовков админки
admin.site.site_header = "TochkaFilms Администрирование"
admin.site.site_title = "TochkaFilms Admin"
admin.site.index_title = "Добро пожаловать в панель управления TochkaFilms"


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date", "birth_place", "age", "get_films_count", "photo_preview"]
    list_filter = ["birth_date", "birth_place"]
    search_fields = ["name", "birth_place", "biography"]
    filter_horizontal = []
    readonly_fields = ["age", "created_at", "updated_at", "photo_preview"]
    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "birth_date", "birth_place", "height")
        }),
        ("Медиа", {
            "fields": ("photo", "photo_preview")
        }),
        ("Описание", {
            "fields": ("biography", "awards")
        }),
        ("Системная информация", {
            "fields": ("age", "created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )

    def age(self, obj):
        return f"{obj.age} лет"
    age.short_description = "Возраст"

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%;" />',
                obj.photo.url
            )
        return "Нет фото"
    photo_preview.short_description = "Превью фото"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "films_count"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def films_count(self, obj):
        count = obj.films.count()
        if count > 0:
            url = reverse("admin:films_film_changelist") + f"?categories__id__exact={obj.id}"
            return format_html('<a href="{}">{} фильм{}</a>', url, count, self.pluralize_films(count))
        return "0 фильмов"
    films_count.short_description = "Количество фильмов"

    def pluralize_films(self, count):
        if count % 10 == 1 and count % 100 != 11:
            return ""
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "а"
        else:
            return "ов"


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ["title", "year", "rating", "duration_display", "is_featured", "poster_preview", "has_trailer", "created_at"]
    list_filter = ["is_featured", "year", "categories", "actors", "rating"]
    search_fields = ["title", "description"]
    filter_horizontal = ["categories", "actors"]
    list_editable = ["is_featured", "rating"]
    readonly_fields = ["poster_preview", "trailer_preview", "created_at", "updated_at"]
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "description", "year", "duration", "rating", "is_featured")
        }),
        ("Медиа", {
            "fields": ("poster", "poster_preview", "trailer_url", "trailer_preview", "video_file")
        }),
        ("Связи", {
            "fields": ("categories", "actors")
        }),
        ("Системная информация", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )

    def duration_display(self, obj):
        hours = obj.duration // 60
        minutes = obj.duration % 60
        if hours > 0:
            return f"{hours}ч {minutes}м"
        return f"{minutes}м"
    duration_display.short_description = "Длительность"

    def poster_preview(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="width: 80px; height: 120px; object-fit: cover;" />',
                obj.poster.url
            )
        return "Нет постера"
    poster_preview.short_description = "Превью постера"

    def trailer_preview(self, obj):
        if obj.trailer_url:
            return format_html(
                '<a href="{}" target="_blank">🎬 Смотреть трейлер</a>',
                obj.trailer_url
            )
        return "Нет трейлера"
    trailer_preview.short_description = "Трейлер"

    def has_trailer(self, obj):
        if obj.trailer_url:
            return format_html('<span style="color: green;">✅</span>')
        return format_html('<span style="color: red;">❌</span>')
    has_trailer.short_description = "Трейлер"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "favorites_count", "watchlist_count"]
    filter_horizontal = ["favorites", "watchlist"]
    search_fields = ["user__username", "user__email"]

    def favorites_count(self, obj):
        return obj.favorites.count()
    favorites_count.short_description = "Избранное"

    def watchlist_count(self, obj):
        return obj.watchlist.count()
    watchlist_count.short_description = "Список просмотра"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["film", "user", "rating", "comment_preview", "created_at"]
    list_filter = ["rating", "created_at", "film__categories"]
    search_fields = ["film__title", "user__username", "comment"]
    readonly_fields = ["created_at"]

    def comment_preview(self, obj):
        if obj.comment:
            return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
        return "Без комментария"
    comment_preview.short_description = "Комментарий"


@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "film", "film_rating", "viewed_at"]
    list_filter = ["viewed_at", "film__categories"]
    search_fields = ["user__username", "film__title"]
    readonly_fields = ["viewed_at"]

    def film_rating(self, obj):
        return f"⭐ {obj.film.rating}"
    film_rating.short_description = "Рейтинг фильма"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "type", "title", "is_read", "created_at"]
    list_filter = ["type", "is_read", "created_at"]
    search_fields = ["user__username", "title", "message"]
    readonly_fields = ["created_at"]
    list_editable = ["is_read"]

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Отметить как прочитанные"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Отметить как непрочитанные"

    actions = [mark_as_read, mark_as_unread]
