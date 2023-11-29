from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.customer.tasks import send_activation_sms, send_confirmation_email
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet 
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAuthor
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer
from rest_framework.decorators import action
from apps.feedback.models import Favorite
from apps.feedback.serializers import FavoriteSerializer


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serialier = RegisterSerializer(data=request.data)
        serialier.is_valid(raise_exception=True)
        user = serialier.save()
        if user:
            try:
                send_confirmation_email.delay(user.email, user.activation_code)
            except:
                return Response({'message': 'Registered, but troubles with email', 'data': serialier.data}, status=201)
        return Response(serialier.data, status=201)
    


class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(Customer, activation_code=code)
        user.is_active = True 
        user.activation_code = ''
        user.save()
        return Response('Succesfuly activated', status=200)
    

class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )


class RegistrationPhoneView(GenericAPIView):
    serializer_class = RegisterSerializer 

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_sms.delay(user.phone_number, user.activation_code)
            return Response('Seccsefully registered', status=201)
        

class ActivationPhoneView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = Customer.objects.filter(phone_number=phone, activation_code=code).first()
        if not user:
            return Response('No such user', status=400)
        user.activation_code = ''
        user.is_active = True 
        user.save()
        return Response('Succesfuly activated', status=200)
    



class StandartPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = UserSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('balance', )
    filterset_fields = ('balance', )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticatedOrReadOnly()]    
    

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def favorites(self, request, pk=None):
        if request.method == 'GET':
            favorites = Favorite.objects.filter(customer_id=pk)
            serializer = FavoriteSerializer(instance=favorites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            user = request.user
            favorite_data = {'freelancer': pk, 'customer': user.id}
            serializer = FavoriteSerializer(data=favorite_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user = request.user  
            favorite = Favorite.objects.filter(freelancer_id=pk, customer=user).first()
            if favorite:
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)
