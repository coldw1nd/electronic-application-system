from django.urls import path

from users import views

app_name = "users"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:user_id>/", views.detail, name="detail"),
]
