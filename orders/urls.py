from django.urls import path
from . import views


app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("success/<int:order_id>", views.successful_order, name="successful_order"),
]
