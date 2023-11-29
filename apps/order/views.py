from django.shortcuts import render
from .models import Order 
from rest_framework.viewsets import ModelViewSet 
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permission import IsAuthor
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
import logging 

logger = logging.getLogger(__name__)

class StandartPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('freelancer', )
    filterset_fields = ('price', 'created_at')

    def perform_create(self, serializer):
        logger.info(self.request.user)
        if hasattr(self.request.user, 'freelancer'):
            raise PermissionDenied("You don't have permission to create an order.")

        serializer.save(customer=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticatedOrReadOnly()]   