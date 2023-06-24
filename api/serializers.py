from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'phone_number')

class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        return user

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password', 'name', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class SearchResultSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.IntegerField(source='get_spam_likelihood')
    email = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'spam_likelihood', 'email']

    def get_email(self, obj):
        user = self.context.get('user')
        if user and obj.isRegistered and user in obj.userID.contacts.all():
            return obj.userID.email
        return None

