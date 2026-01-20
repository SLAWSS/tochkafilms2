from django.db.models import Q
from .models import Film


def get_similar_films(film, limit=6):
    """Получает похожие фильмы на основе категорий и года"""
    # Получаем категории текущего фильма
    film_categories = film.categories.all()
    
    if not film_categories:
        return Film.objects.exclude(pk=film.pk).order_by('-rating')[:limit]
    
    # Ищем фильмы с похожими категориями
    similar_films = Film.objects.filter(
        categories__in=film_categories
    ).exclude(pk=film.pk).distinct()
    
    # Сортируем по рейтингу и близости по году
    year_range = 10  # ±10 лет
    similar_films = similar_films.filter(
        year__gte=film.year - year_range,
        year__lte=film.year + year_range
    ).order_by('-rating')
    
    # Если мало фильмов, расширяем поиск
    if similar_films.count() < limit:
        additional_films = Film.objects.filter(
            categories__in=film_categories
        ).exclude(pk=film.pk).exclude(
            pk__in=similar_films.values_list('pk', flat=True)
        ).distinct().order_by('-rating')
        
        similar_films = list(similar_films) + list(additional_films)
    
    return similar_films[:limit]


def get_recommended_films(user, limit=8):
    """Получает рекомендованные фильмы для пользователя"""
    if not user.is_authenticated:
        return Film.objects.filter(is_featured=True).order_by('-rating')[:limit]
    
    try:
        profile = user.profile
        favorite_categories = set()
        
        # Анализируем избранные фильмы
        for film in profile.favorites.all():
            favorite_categories.update(film.categories.all())
        
        # Анализируем список просмотра
        for film in profile.watchlist.all():
            favorite_categories.update(film.categories.all())
        
        if favorite_categories:
            # Рекомендуем фильмы из любимых категорий
            recommended = Film.objects.filter(
                categories__in=favorite_categories
            ).exclude(
                pk__in=profile.favorites.values_list('pk', flat=True)
            ).exclude(
                pk__in=profile.watchlist.values_list('pk', flat=True)
            ).distinct().order_by('-rating')[:limit]
            
            if recommended.count() >= limit:
                return recommended
        
        # Если недостаточно, добавляем популярные
        return Film.objects.filter(is_featured=True).order_by('-rating')[:limit]
        
    except:
        return Film.objects.filter(is_featured=True).order_by('-rating')[:limit]


def get_top_films_by_category():
    """Получает топ фильмов по категориям"""
    from .models import Category
    
    top_films = {}
    for category in Category.objects.all():
        top_films[category] = category.films.order_by('-rating')[:5]
    
    return top_films