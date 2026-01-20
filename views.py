from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Film, Category, Actor, UserProfile, Review, ViewHistory, Notification
from .utils import get_similar_films, get_recommended_films, get_top_films_by_category


def home(request):
    featured_films = Film.objects.filter(is_featured=True)[:6]
    recent_films = Film.objects.all().order_by('-created_at')[:12]
    categories = Category.objects.all()
    
    # Персональные рекомендации
    recommended_films = get_recommended_films(request.user, 6)
    
    # История просмотров для авторизованных пользователей
    recent_viewed = []
    if request.user.is_authenticated:
        recent_viewed = ViewHistory.objects.filter(
            user=request.user
        ).select_related('film')[:6]
    
    context = {
        "featured_films": featured_films,
        "recent_films": recent_films,
        "categories": categories,
        "recommended_films": recommended_films,
        "recent_viewed": recent_viewed,
    }
    return render(request, "films/home.html", context)


def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    reviews = film.reviews.all().order_by("-created_at")
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    
    user_profile = None
    is_favorite = False
    is_in_watchlist = False
    
    if request.user.is_authenticated:
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        is_favorite = user_profile.favorites.filter(pk=film.pk).exists()
        is_in_watchlist = user_profile.watchlist.filter(pk=film.pk).exists()
        
        # Добавляем в историю просмотров
        ViewHistory.objects.get_or_create(user=request.user, film=film)
    
    # Похожие фильмы
    similar_films = get_similar_films(film, 6)
    
    context = {
        "film": film,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "is_favorite": is_favorite,
        "is_in_watchlist": is_in_watchlist,
        "similar_films": similar_films,
    }
    return render(request, "films/film_detail.html", context)


def category_films(request, slug):
    category = get_object_or_404(Category, slug=slug)
    films = category.films.all()
    
    context = {
        "category": category,
        "films": films,
    }
    return render(request, "films/category_films.html", context)


def search(request):
    query = request.GET.get("q", "").strip()
    films = []
    
    if query:
        from django.db.models import Value
        from django.db.models.functions import Lower
        
        # Приводим запрос к нижнему регистру для поиска
        query_lower = query.lower()
        
        # Получаем все фильмы и фильтруем их в Python для надежности
        all_films = Film.objects.all().prefetch_related('categories')
        matching_films = []
        
        for film in all_films:
            # Проверяем название фильма
            if query_lower in film.title.lower():
                matching_films.append(film.id)
                continue
                
            # Проверяем описание
            if query_lower in film.description.lower():
                matching_films.append(film.id)
                continue
                
            # Проверяем категории
            for category in film.categories.all():
                if query_lower in category.name.lower():
                    matching_films.append(film.id)
                    break
            
            # Проверяем год
            if query.isdigit() and query in str(film.year):
                matching_films.append(film.id)
                continue
        
        # Если найдены совпадения, получаем фильмы из базы
        if matching_films:
            films = Film.objects.filter(id__in=matching_films).distinct()
        
        # Если ничего не найдено, попробуем поиск по частям слов
        if not matching_films and len(query) > 2:
            words = query_lower.split()
            for word in words:
                if len(word) > 1:
                    for film in all_films:
                        if (word in film.title.lower() or 
                            word in film.description.lower() or
                            any(word in cat.name.lower() for cat in film.categories.all())):
                            matching_films.append(film.id)
            
            if matching_films:
                films = Film.objects.filter(id__in=matching_films).distinct()
    
    context = {
        "query": query,
        "films": films,
        "films_count": films.count() if films else 0,
    }
    return render(request, "films/search.html", context)


@login_required
def toggle_favorite(request, pk):
    film = get_object_or_404(Film, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if profile.favorites.filter(pk=film.pk).exists():
        profile.favorites.remove(film)
    else:
        profile.favorites.add(film)
    
    return redirect("films:film_detail", pk=pk)


@login_required
def toggle_watchlist(request, pk):
    film = get_object_or_404(Film, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if profile.watchlist.filter(pk=film.pk).exists():
        profile.watchlist.remove(film)
    else:
        profile.watchlist.add(film)
    
    return redirect("films:film_detail", pk=pk)


@login_required
def my_list(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    favorites = profile.favorites.all()
    watchlist = profile.watchlist.all()
    
    context = {
        "favorites": favorites,
        "watchlist": watchlist,
    }
    return render(request, "films/my_list.html", context)


@login_required
def add_review(request, pk):
    if request.method == "POST":
        film = get_object_or_404(Film, pk=pk)
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")
        
        Review.objects.update_or_create(
            film=film,
            user=request.user,
            defaults={"rating": rating, "comment": comment}
        )
    
    return redirect("films:film_detail", pk=pk)


def top_films(request):
    """Страница топ фильмов"""
    # Общий топ
    top_rated = Film.objects.order_by('-rating')[:10]
    most_popular = Film.objects.annotate(
        views_count=Count('views')
    ).order_by('-views_count')[:10]
    
    # Топ по категориям
    top_by_category = get_top_films_by_category()
    
    context = {
        "top_rated": top_rated,
        "most_popular": most_popular,
        "top_by_category": top_by_category,
    }
    return render(request, "films/top_films.html", context)


def films_filter(request):
    """Фильтрация фильмов"""
    films = Film.objects.all()
    
    # Фильтры
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    rating_from = request.GET.get('rating_from')
    category_id = request.GET.get('category')
    sort_by = request.GET.get('sort', '-rating')
    
    if year_from:
        films = films.filter(year__gte=year_from)
    if year_to:
        films = films.filter(year__lte=year_to)
    if rating_from:
        films = films.filter(rating__gte=rating_from)
    if category_id:
        films = films.filter(categories__id=category_id)
    
    # Сортировка
    if sort_by in ['-rating', 'rating', '-year', 'year', 'title', '-title']:
        films = films.order_by(sort_by)
    
    # Пагинация
    paginator = Paginator(films.distinct(), 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        "page_obj": page_obj,
        "categories": categories,
        "current_filters": {
            "year_from": year_from,
            "year_to": year_to,
            "rating_from": rating_from,
            "category": category_id,
            "sort": sort_by,
        }
    }
    return render(request, "films/films_filter.html", context)


@login_required
def view_history(request):
    """История просмотров пользователя"""
    history = ViewHistory.objects.filter(
        user=request.user
    ).select_related('film').order_by('-viewed_at')
    
    paginator = Paginator(history, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
    }
    return render(request, "films/view_history.html", context)


@login_required
def notifications(request):
    """Уведомления пользователя"""
    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Отмечаем как прочитанные
    user_notifications.filter(is_read=False).update(is_read=True)
    
    paginator = Paginator(user_notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
    }
    return render(request, "films/notifications.html", context)


@login_required
def clear_history(request):
    """Очистка истории просмотров"""
    if request.method == "POST":
        ViewHistory.objects.filter(user=request.user).delete()
    return redirect("films:view_history")


def get_notifications_count(request):
    """API для получения количества непрочитанных уведомлений"""
    if not request.user.is_authenticated:
        return JsonResponse({"count": 0})
    
    count = Notification.objects.filter(
        user=request.user, 
        is_read=False
    ).count()
    
    return JsonResponse({"count": count})


def actors_list(request):
    """Список всех актеров"""
    actors = Actor.objects.all().annotate(
        films_count=Count('films')
    ).order_by('name')
    
    # Пагинация
    paginator = Paginator(actors, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "actors": page_obj,
    }
    return render(request, "films/actors_list.html", context)


def actor_detail(request, pk):
    """Детальная страница актера"""
    actor = get_object_or_404(Actor, pk=pk)
    films = actor.films.all().order_by('-year')
    
    context = {
        "actor": actor,
        "films": films,
        "films_count": films.count(),
    }
    return render(request, "films/actor_detail.html", context)


def actors_search(request):
    """Поиск актеров"""
    query = request.GET.get("q", "").strip()
    actors = []
    
    if query:
        actors = Actor.objects.filter(
            Q(name__icontains=query) |
            Q(birth_place__icontains=query) |
            Q(biography__icontains=query)
        ).annotate(
            films_count=Count('films')
        ).distinct()
    
    context = {
        "query": query,
        "actors": actors,
        "actors_count": actors.count() if actors else 0,
    }
    return render(request, "films/actors_search.html", context)