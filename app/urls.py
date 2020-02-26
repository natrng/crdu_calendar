from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('logout', views.logout),
    path('login', views.login),
    path('success', views.CalendarView.as_view()),
    path('calendar/new', views.create),
    path('calendar/<int:id>', views.view),
    path('calendar/delete/<int:id>', views.delete_event),
    path('calendar/edit/<int:id>', views.edit),
    path('calendar/update/<int:id>', views.update),
]