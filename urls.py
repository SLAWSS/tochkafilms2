from django.urls import path
from . import views

app_name = "films"

urlpatterns = [
    path("", views.home, name="home"),
    path("film/<int:pk>/", views.film_detail, name="film_detail"),
    path("category/<slug:slug>/", views.category_films, name="category_films"),
    path("search/", views.search, name="search"),
    path("my-list/", views.my_list, name="my_list"),
    path("film/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("film/<int:pk>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("film/<int:pk>/review/", views.add_review, name="add_review"),
    
    # Актеры
    path("actors/", views.actors_list, name="actors_list"),
    path("actor/<int:pk>/", views.actor_detail, name="actor_detail"),
    path("actors/search/", views.actors_search, name="actors_search"),
    
    # Новые функции
    path("top/", views.top_films, name="top_films"),
    path("filter/", views.films_filter, name="films_filter"),
    path("history/", views.view_history, name="view_history"),
    path("history/clear/", views.clear_history, name="clear_history"),
    path("notifications/", views.notifications, name="notifications"),
    path("api/notifications-count/", views.get_notifications_count, name="notifications_count"),
]
