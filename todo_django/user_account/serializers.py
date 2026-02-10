from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles creating new user accounts with password validation.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'email',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': False},
        }

    def validate_password(self, value):
        """
        Validate password strength:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        """
        errors = []

        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")

        if not any(char.isupper() for char in value):
            errors.append("Password must contain at least one uppercase letter.")

        if not any(char.islower() for char in value):
            errors.append("Password must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one number.")

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate_email(self, value):
        """
        Validate email is unique if provided.
        """
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_username(self, value):
        """
        Validate username:
        - Must be unique
        - No special characters
        - Only letters, numbers, and underscores
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )

        return value

    def validate(self, data):
        """
        Validate that passwords match.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match."
            })
        return data

    def create(self, validated_data):
        """
        Create and return new user.
        Remove password_confirm before creating user.
        """
        # Remove password_confirm (not a model field)
        validated_data.pop('password_confirm')

        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data.get('email', None),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates credentials and returns user object.
    """
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        """
        Validate username and password.
        """
        username = data.get('username')
        password = data.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "username": "No account found with this username."
            })

        # Authenticate user
        user = authenticate(username=username, password=password)

        # Check if password is correct
        if not user:
            raise serializers.ValidationError({
                "password": "Incorrect password."
            })

        # Check if account is active
        if not user.is_active:
            raise serializers.ValidationError({
                "username": "This account has been deactivated."
            })

        # Add user to validated data
        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user profile.
    Username can only be changed once every 2 weeks.
    """
    days_until_username_change = serializers.SerializerMethodField()
    can_change_username = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'date_joined',
            'last_login',
            'can_change_username',
            'days_until_username_change',
        ]
        read_only_fields = [
            'id',
            'date_joined',
            'last_login',
            'can_change_username',
            'days_until_username_change',
            'full_name',
        ]
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def get_days_until_username_change(self, obj):
        """
        Returns how many days until username can be changed.
        Returns 0 if username can be changed now.
        """
        return obj.days_until_username_change()

    def get_can_change_username(self, obj):
        """
        Returns whether user can change their username.
        """
        return obj.can_change_username()

    def get_full_name(self, obj):
        """
        Returns user's full name.
        """
        return obj.get_full_name()

    def validate_username(self, value):
        """
        Validate username change:
        - Must be unique
        - No special characters
        - Cannot change if within 2 week restriction
        """
        user = self.instance

        # Check if username is actually being changed
        if user.username == value:
            return value

        # Check 2 week restriction
        if not user.can_change_username():
            days_left = user.days_until_username_change()
            raise serializers.ValidationError(
                f"You cannot change your username yet. "
                f"Please wait {days_left} more day(s)."
            )

        # Check uniqueness
        if User.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        # Check no special characters
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )

        return value

    def validate_email(self, value):
        """
        Validate email is unique if changed.
        """
        user = self.instance

        # Check if email is actually being changed
        if user.email == value:
            return value

        # Check uniqueness
        if value and User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def update(self, instance, validated_data):
        """
        Update user profile.
        If username is changed, update last_username_change timestamp.
        """
        # Check if username is being changed
        new_username = validated_data.get('username', instance.username)
        if new_username != instance.username:
            instance.last_username_change = timezone.now()

        # Update all other fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance