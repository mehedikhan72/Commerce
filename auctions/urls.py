from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing/<str:listed_by>", views.create_list, name="create_listing"),
    path("details/<str:item>", views.details, name="details"),
    path("watchlist/<str:current_user>", views.watchlist, name="watchlist"),
    path("details/<int:id>/<str:current_user>/addtowatchlist", views.addtowatchlist, name="addtowatchlist"),
    path("details/<int:id>/<str:current_user>/removefromwatchlist", views.removefromwatchlist, name="removefromwatchlist"),
    path("details/<str:item>/add_comments", views.addcomments, name="addcomments"), 
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_items, name="category_items"),
    path("details/<str:item>/bid", views.bidding, name="bidding")
]
