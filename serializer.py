from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User

from master.serializer import CompanyMasterSerializer, DepoMasterSerializer
from accounts.models import UserMaster, RoleMaster


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', "is_superuser", "username", "is_active", "password")


class UserMasterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserMaster
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            role_instance = validated_data.get('role')
            is_staff = role_instance.role_name == "DepoAdmin"
            user_instance = User.objects.create(
                username=user_data['username'],
                password=make_password(user_data['password']),
                is_superuser=user_data['is_superuser'],
                is_staff=is_staff
            )
            user_master_instance = UserMaster.objects.create(user=user_instance, **validated_data)
            return user_master_instance

    # def update(self, instance, validated_data):
    #     user_data = validated_data.get('user')
    #     if user_data:
    #         user_instance = instance.user
    #         user_instance.username = user_data.get('username', user_instance.username)
    #         user_instance.password = make_password(user_data.get('password', user_instance.password))
    #         user_instance.save()
    #     instance.save()
    #     return instance

class UserListSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='comapny.company_name')
    depo = serializers.CharField(source='depo.depo_name')
    role = serializers.CharField(source='role.role_name')
    username = serializers.CharField(source='user.username')
    class Meta:
        model = UserMaster
        fields = ['id', 'username', 'user_code', 'first_name', 'last_name', 'email', 'mobile_no', 'address', 'city', 'district', 'pincode', 'is_active', 'created_date', 'updated_date', 'company', 'depo','role']

class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = "__all__"

class UpdateUserMasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = ['first_name','last_name','email','mobile_no',
                  'address','city','district','pincode','comapny','depo','role']
