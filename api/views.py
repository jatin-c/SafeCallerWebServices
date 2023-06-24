from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, Contact
from .serializers import UserRegistrationSerializer, ContactSerializer, SearchResultSerializer
from .authentication import CustomJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import ContactSerializer, SearchResultSerializer
from django.db.models import Q

# from rest_framework_simplejwt.tokens import RefreshToken

        

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        # Verify the validity and expiration of the refresh token
        try:
            refresh = RefreshToken(refresh_token)
            refresh_token = refresh.refresh_token
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)
        
        # Generate a new access token
        access_token = refresh.access_token
        
        return Response({'access_token': str(access_token)})


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                return Response({'error': 'A user with this phone number already exists.'}, status=400)
            user = serializer.save()
            return Response({'message': 'User registered successfully.'})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        User = get_user_model()
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=401)

        if not check_password(password, user.password):
            return Response({'error': 'Invalid credentials'}, status=401)

        # Generate token for the user
        refresh = RefreshToken.for_user(user)

        # Return the token as a response
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        })


def check_token_validity(token):
    try:
        refresh_token = RefreshToken(token)
        access_token = refresh_token.access_token
        is_access_token_valid = access_token.is_valid()
        is_refresh_token_valid = refresh_token.is_valid()
        
        return is_access_token_valid, is_refresh_token_valid
    except Exception as e:
        return False, False
    
class MarkSpamView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')

        # Check if the contact exists for the current user
        try:
            contact = Contact.objects.get(phone_number=phone_number, userID=request.user)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=404)

        # Mark the contact as spam
        contact.isSpam = True
        contact.save()

        return Response({'message': 'Phone number marked as spam'}, status=200)
    
def get_user(validated_token):
        # print(validated_token['sub'])
        User = get_user_model()
        try:
            user_id = validated_token['user_id']
            return User.objects.get(pk=user_id)
        except (User.DoesNotExist, KeyError):
            raise InvalidToken('Token contained invalid user identification.')
# import jwt

# Assuming 'access_token' holds the actual token value

class AddContactView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomJWTAuthentication]
    
    def post(self, request):
        # print(request.auth)
        # validated_token = AccessToken(request.auth)
        
        # Use the custom authentication class to get the user instance
        # user = get_user(request.auth)
        serializer = ContactSerializer(data=request.data)
       
        if serializer.is_valid():
            # Set the user ID of the contact to the current logged-in user
            # user = get_user(serializer.validated_data)

            serializer.validated_data['userID'] = request.user

            # Save the contact
            serializer.save()

            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    
class SearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')

        # Search by name
        name_results = Contact.objects.filter(
            Q(name__istartswith=query) | Q(name__icontains=query),
            isRegistered=True
        ).order_by('name')

        # Search by phone number
        phone_results = Contact.objects.filter(
            phone_number=query
        )

        result_list = []
        result_list.extend(name_results)
        result_list.extend(phone_results)

        # Serialize search results
        serializer = SearchResultSerializer(result_list, many=True)
        return Response(serializer.data, status=200)






