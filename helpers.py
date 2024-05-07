import json
import logging
import requests
from django.db import transaction
from TML_DEPO import settings
from commons import error_conf, system_errors, utils
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from accounts.serializer import RoleListSerializer, UpdateUserMasterDataSerializer, UserSerializer, \
    UserMasterSerializer, UserListSerializer
from accounts.models import RoleMaster, UserMaster
from logging.config import dictConfig
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

api_logger = logging.getLogger('api_logger')


def login_with_password(self, data):
    try:
        # Get the data
        if data:
            username = data.get('login_name', '')
            password = data.get('password', '')

            if not username:
                return Response(error_conf.USERNAME_NOT_PROVIDED,
                                status=status.HTTP_412_PRECONDITION_FAILED)

            if not password:
                return Response(error_conf.PASSWORD_NOT_PROVIDED,
                                status=status.HTTP_412_PRECONDITION_FAILED)

            # Getting the user
            try:
                user_obj = User.objects.get(username=username)
                if not user_obj.is_active:
                    return Response(error_conf.CONTACT_TML_ADMIN_PORTAL_TO_ACTIVE,
                                    status=status.HTTP_412_PRECONDITION_FAILED)
                if user_obj.is_superuser:
                    return Response(error_conf.USER_NOT_AUTHORIZED,
                                    status=status.HTTP_412_PRECONDITION_FAILED)
                user_password = user_obj.password
                user_data = UserMaster.objects.filter(user=user_obj).first()
                # Checking the password
                if not check_password(password, user_password):
                    return Response(error_conf.INVALID_LOGIN_DETAILS,
                                    status=status.HTTP_412_PRECONDITION_FAILED)

                # Getting the token
                client_id = settings.AUTH_CLIENT_ID
                client_secret = settings.AUTH_CLIENT_SECRET
                host = self.request.get_host()
                token_url = settings.SERVER_HOST_PROTOCOL + host + settings.TOKEN_ENDPOINT
                data = utils.generate_oauth_token(username, password, client_id, client_secret, token_url)

                if data.status_code == 200:
                    token_data = json.loads(data.content.decode("utf-8"))
                    user_serializer = UserMasterSerializer(user_data)
                    response_data = {
                        "success": True,
                        "token": token_data,
                        "data": user_serializer.data
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Failed to obtain OAuth token'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except User.DoesNotExist:
                return Response(error_conf.USER_DOES_NOT_EXIST,
                                status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            return Response(error_conf.DATA_NOT_PROVIDED,
                            status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG,
                        status=status.HTTP_412_PRECONDITION_FAILED)


def logout_user(self, user, token):
    try:
        access_token = token
        client_id = settings.AUTH_CLIENT_ID
        client_secret = settings.AUTH_CLIENT_SECRET
        host = self.request.get_host()
        revoke_token_url = settings.SERVER_HOST_PROTOCOL + host + '/o/revoke_token/'
        data = utils.revoke_oauth_token(access_token, client_id, client_secret, revoke_token_url)
        api_logger.info(data.status_code)
        if data.status_code != 200:
            return Response({'error': 'Failed to obtain OAuth token'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        api_logger.info('User logout successfully!')
        return Response(error_conf.USER_LOGOUT, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG,
                        status=status.HTTP_412_PRECONDITION_FAILED)


def register_user(self, data):
    try:
        with transaction.atomic():
            user_data = {
                "username": data.get("username"),
                "password": data.get("password"),
                "is_active": True,
                "is_superuser": False,
                "is_staff": False
            }
            user_master_data = {
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "mobile_no": data.get("phone"),
                "address": data.get("address"),
                "city": data.get("city"),
                "district": data.get("district"),
                "pincode": data.get("pincode"),
                "user": user_data
            }
            email = data.get("email", "")
            #checked if email already exists or not 
            if UserMaster.objects.filter(user__email=email).exists():
                return Response(error_conf.USER_ALREADY_EXISTS, status=status.HTTP_200_OK)
            user_master_data["email"] = email
            company = data.get("company")
            depo = data.get("depo")
            role = data.get("role")

            company_instance = utils.get_company_instance(company)
            depo_instance = utils.get_depo_instance(depo)
            role_instance = utils.get_role_instance(role)

            if not company_instance:
                return Response(error_conf.COMPANY_DOES_NOT_EXIST,
                                status=status.HTTP_412_PRECONDITION_FAILED)
            if not depo_instance:
                return Response(error_conf.DEPO_DOES_NOT_EXIST,
                                status=status.HTTP_412_PRECONDITION_FAILED)
            if not role_instance:
                return Response(error_conf.ROLE_DOES_NOT_EXIST,
                                status=status.HTTP_412_PRECONDITION_FAILED)

            if role_instance.role_name == "DepoAdmin":
                user_data["is_superuser"] = True
                user_data["is_staff"] = True

            user_master_data["role"] = role_instance.id
            user_master_data["comapny"] = company_instance.id
            user_master_data["depo"] = depo_instance.id

            last_user = UserMaster.objects.order_by("-user_code").first()
            if last_user is None:
                new_code = 'U001'
            else:
                new_code = utils.create_code_for_user(last_user)
            user_master_data['user_code'] = new_code
            serializer = UserMasterSerializer(data=user_master_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_412_PRECONDITION_FAILED)
            serializer.save()
            return Response(error_conf.USER_CREATED_SUCCESSFULLY, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)


def get_refresh_token(self, data):
    try:
        refresh_token = data.get("refresh_token")

        if not refresh_token:
            return Response(
                data=error_conf.REFRESH_TOKEN_NOT_PROVIDED,
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        client_id = settings.AUTH_CLIENT_ID
        client_secret = settings.AUTH_CLIENT_SECRET
        refresh_token = str(self.request.data.get("refresh_token"))
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "token type": "Bearer",
            "refresh_token": refresh_token
        }
        host = self.request.get_host()
        url = settings.SERVER_HOST_PROTOCOL + host + settings.TOKEN_ENDPOINT
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            formatted_data = {
                "success": True,
                "data": data
            }
            return Response(
                data=formatted_data, status=status.HTTP_200_OK)
        else:
            return Response(error_conf.INVALID_REFRESH_TOKEN,
                            status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)


def get_user_list(self, data):
    try:
        limit = int(data.get('limit', 10))  # Default limit is 10
        offset = int(data.get('offset', 0))  # Default offset is 0
        first_name = data.get('first_name', '')
        user_code = data.get('user_code', '')

        user_kwargs = {"is_active": True}
        if first_name:
            user_kwargs['first_name__icontains'] = first_name

        if user_code:
            user_kwargs['user_code__icontains'] = user_code

        queryset = UserMaster.objects.filter(**user_kwargs)

        total = queryset.count()
        user_list = queryset.order_by('-id')[offset:offset + limit]

        if not user_list.exists():
            return Response(error_conf.DATA_NOT_FOUND, status=status.HTTP_200_OK)

        serializer = UserListSerializer(user_list, many=True)
        return Response({'total': total, 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)


def get_role_list(self, data):
    try:
        limit = int(data.get('limit', 10))  # Default limit is 10
        offset = int(data.get('offset', 0))  # Default offset is 0
        role_name = data.get('role_name', '')
        kwargs = {'is_active': True}
        if role_name:
            kwargs['role_name'] = role_name
        total = RoleMaster.objects.filter(**kwargs).count()
        if total == 0:
            return Response(error_conf.DATA_NOT_FOUND, status=status.HTTP_200_OK)
        roles = RoleMaster.objects.filter(**kwargs)[offset:offset + limit]
        serializer = RoleListSerializer(roles, many=True)
        return Response({'total': total, 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)


def update_user_data(data):
    """_summary_

    first we get the user id and then filter from db
    if exits then we continue else return error
    second get the updating data and update according to

    """

    user_id = data.get('user_id', '')
    update_user_kwargs = {}

    if not user_id:
        return Response(
            data=error_conf.USER_ID_NOT_PROVIDED,
            status=status.HTTP_412_PRECONDITION_FAILED
        )

    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    email = data.get('email', '')
    mobile_no = data.get('mobile_no', '')
    address = data.get('address', '')
    city = data.get('city', '')
    district = data.get('district', '')
    pincode = data.get('pincode', '')
    company = data.get('company', '')
    depo = data.get('depo', '')
    role = data.get('role', '')

    # getting the user instance
    user_instance = utils.get_usermaster_instance(int(user_id))

    if not user_instance:
        return Response(error_conf.USER_DOES_NOT_EXIST,
                        status=status.HTTP_412_PRECONDITION_FAILED)

    if company:
        company_instance = utils.get_company_instance(company)
        if not company_instance:
            return Response(error_conf.COMPANY_DOES_NOT_EXIST,
                            status=status.HTTP_412_PRECONDITION_FAILED)
        update_user_kwargs['comapny'] = company_instance.id

    if depo:
        depo_instance = utils.get_depo_instance(depo)
        if not depo_instance:
            return Response(error_conf.DEPO_DOES_NOT_EXIST,
                            status=status.HTTP_412_PRECONDITION_FAILED)
        update_user_kwargs['depo'] = depo_instance.id

    if role:
        role_instance = utils.get_role_instance(role)

        if not role_instance:
            return Response(error_conf.ROLE_DOES_NOT_EXIST,
                            status=status.HTTP_412_PRECONDITION_FAILED)
        update_user_kwargs['role'] = role_instance.id

    # updating the data

    if first_name:
        update_user_kwargs['first_name'] = first_name

    if last_name:
        update_user_kwargs['last_name'] = last_name

    if email:
        update_user_kwargs['email'] = email

    if mobile_no:
        update_user_kwargs['mobile_no'] = mobile_no

    if address:
        update_user_kwargs['address'] = address

    if city:
        update_user_kwargs['city'] = city

    if district:
        update_user_kwargs['district'] = district

    if pincode:
        update_user_kwargs['pincode'] = pincode

    try:
        serializer = UpdateUserMasterDataSerializer(user_instance, data=update_user_kwargs, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(error_conf.USER_UPDATED_SUCCESSFULLY, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)


def admin_login_with_password(self, data):
    try:
        # Get the data
        if data:
            username = data.get('login_name', '')
            password = data.get('password', '')

            if not username:
                return Response(error_conf.USERNAME_NOT_PROVIDED,
                                status=status.HTTP_412_PRECONDITION_FAILED)

            if not password:
                return Response(error_conf.PASSWORD_NOT_PROVIDED,
                                status=status.HTTP_412_PRECONDITION_FAILED)

            # Getting the user
            try:
                user_obj = User.objects.get(username=username)
                if not user_obj.is_active:
                    return Response(error_conf.CONTACT_TML_ADMIN_PORTAL_TO_ACTIVE,
                                    status=status.HTTP_412_PRECONDITION_FAILED)

                user_password = user_obj.password

                # Checking the password
                if not check_password(password, user_password):
                    return Response(error_conf.INVALID_LOGIN_DETAILS,
                                    status=status.HTTP_412_PRECONDITION_FAILED)

                user_data = UserMaster.objects.filter(user=user_obj).first()
                if user_obj.is_superuser:
                    # Getting the token
                    client_id = settings.AUTH_CLIENT_ID
                    client_secret = settings.AUTH_CLIENT_SECRET
                    host = self.request.get_host()
                    token_url = settings.SERVER_HOST_PROTOCOL + host + settings.TOKEN_ENDPOINT
                    data = utils.generate_oauth_token(username, password, client_id, client_secret, token_url)

                    if data.status_code == 200:
                        token_data = json.loads(data.content.decode("utf-8"))
                        user_serializer = UserMasterSerializer(user_data)
                        response_data = {
                            "success": True,
                            "token": token_data,
                            "data": user_serializer.data
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Failed to obtain OAuth token'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(error_conf.USER_NOT_AUTHORIZED,
                                    status=status.HTTP_412_PRECONDITION_FAILED)
            except User.DoesNotExist:
                return Response(error_conf.USER_DOES_NOT_EXIST,
                                status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            return Response(error_conf.DATA_NOT_PROVIDED,
                            status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG,
                        status=status.HTTP_412_PRECONDITION_FAILED)


def reset_password(data):
    try:
        email = data.get('email', '')

        if not email:
            return Response(error_conf.EMAIL_NOT_PROVIDED,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        user_obj = utils.get_usermaster_instance(email=email).user
        if not user_obj:
            return Response(error_conf.USER_DOES_NOT_EXIST,
                            status=status.HTTP_412_PRECONDITION_FAILED)
        token = default_token_generator.make_token(user_obj)
        uid = urlsafe_base64_encode(force_bytes(user_obj.pk))

        # reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        reset_url = f"http://127.0.0.1:8000/api/depo/v1/reset_password_verify/?uidb64={uid}&token={token}"
        email_dict = {
            'email': email,
            'subject': 'Password Reset TML-DEPO',
            'message': f"CLICK BELOW LINK TO RESET YOUR PASSWORD :\n {reset_url}"
        }
        send_mail = utils.send_mail_to_user(**email_dict)
        if not send_mail:
            return Response(error_conf.SOMETHING_WENT_WRONG,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        return Response(error_conf.EMAIL_SENT_SUCCESSFULLY,
                        status=status.HTTP_200_OK)

    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG,
                        status=status.HTTP_412_PRECONDITION_FAILED)


def reset_password_verify(data, uidb64, token):
    try:
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')

        if not uidb64 or not token:
            return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)

        if not new_password or not confirm_password:
            return Response(error_conf.DATA_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED)

        if new_password != confirm_password:
            return Response(error_conf.PASSWORD_NOT_MATCHED, status=status.HTTP_412_PRECONDITION_FAILED)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            # email = utils.get_usermaster_instance(user_id=uid).email
        except Exception as ex:
            return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response(error_conf.PASSWORD_RESET_SUCCESSFULLY, status=status.HTTP_200_OK)
        else:
            return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)

    except Exception as ex:
        return Response(error_conf.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)
