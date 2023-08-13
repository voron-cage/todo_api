from django.urls import path
from .views import TODOListViewSet, TODOActionViewSet, TODOViewSet

urlpatterns = [
    path('', TODOListViewSet.as_view({'get': 'list', 'post': 'create'}), name='todo-list'),
    path('<slug:slug>/', TODOViewSet.as_view({'get': 'list', 'put': 'update', 'post': 'create'}), name='todo-detail'),
    path('<slug:slug>/<slug:action_slug>/', TODOActionViewSet.as_view({'put': 'update'}), name='todo-action'),
]
