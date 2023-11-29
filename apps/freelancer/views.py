from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from apps.freelancer.tasks import send_activation_sms, send_confirmation_email
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet 
from rest_framework import permissions 
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAuthor
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from apps.feedback.serializers import FreelancerRatingSerializer
from django.http import HttpResponseServerError
from apps.customer.models import Customer
from apps.freelancer.models import Freelancer

User = get_user_model()

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
        user = get_object_or_404(Freelancer, activation_code=code)
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
        user = Freelancer.objects.filter(phone_number=phone, activation_code=code).first()
        if not user:
            return Response('No such user', status=400)
        user.activation_code = ''
        user.is_active = True 
        user.save()
        return Response('Succesfuly activated', status=200)
    



class StandartPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class FreelancerViewSet(ModelViewSet):
    queryset = Freelancer.objects.all()
    serializer_class = UserSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('profession', )
    filterset_fields = ('profession', 'price', 'city', )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticatedOrReadOnly()]    
    
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def rating(self, request, pk):
        freelancer = self.get_object()
        user = request.user
        if not isinstance(user, Customer):
            print(user)
            return HttpResponseServerError("Ошибка: request.user не является экземпляром Customer.")

        if request.method == 'GET':
            ratings = freelancer.ratings.all()
            serializer = FreelancerRatingSerializer(instance=ratings, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if freelancer.ratings.filter(customer=user).exists():
                return Response('You already rated this freelancer', status=400)
            data = request.data
            serializer = FreelancerRatingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=user, freelancer=freelancer)
            return Response(serializer.data, status=201)

        else:
            if not freelancer.ratings.filter(customer=user).exists():
                return Response("You didn't rated this freelancer")
            rating = freelancer.ratings.get(customer=user)
            rating.delete()
            return Response('Deleted', status=204)