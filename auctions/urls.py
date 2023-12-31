from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="new_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/placebid", views.place_bid, name="placebid")
]
