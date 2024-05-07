from rest_framework.views import APIView
import logging
from commons import error_conf, system_errors
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from . import helpers

api_logger = logging.getLogger('api_logger')


class RegisterApiView(APIView):
    """
    Creating API for User Registration
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            data = request.data
            api_logger.info("register api started")
            api_logger.info(request.data)
            return helpers.register_user(self, data)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())


# login api
class LoginApiView(APIView):
    """
    Creating API for User Authentication
    Based On  UserName and Passwords

    """

    def post(self, request):
        """
        Return a Valid token if username and password
        is valid for a given user
        """
        try:
            api_logger.info('Login api initiated with data')

            api_logger.info(request.data)
            return helpers.login_with_password(self, request.data)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())


# logout view
class LogOutView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """_summary_
        delete token of requested user
        """
        try:
            api_logger.info("Logout api started")
            api_logger.info(request.user)
            api_logger.info(request.auth)
            user = request.user
            token = request.auth
            return helpers.logout_user(self, user, token)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())


class RefreshTokenView(APIView):
    def post(self, request):
        """
            this view is used to refresh token
        """
        try:
            api_logger.info("refresh token api started")
            api_logger.info(request.user)
            data = request.data
            return helpers.get_refresh_token(self, data)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())


class TestApiView(APIView):
    def get(self, request, format=None):
        return Response({'message': 'This is a Test API response'}, status=status.HTTP_200_OK)

class UserListApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            api_logger.info("user listing api started")
            data = request.data
            return helpers.get_user_list(self, data)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())


class RoleListApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            api_logger.info("role listing api started")
            data = request.data
            return helpers.get_role_list(self, data)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())


class UpdateUserApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """_summary_

        this api updates the added user information
        """
        try:
            api_logger.info("update user api started")
            api_logger.info(request.user)
            data = request.data
            return helpers.update_user_data(data)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())
        
class AdminLoginApiView(APIView):
    """
    Creating API for Admin User Authentication
    Based On  UserName and Passwords

    """

    def post(self, request):
        """
        Return a Valid token if username and password
        is valid for a given user
        """
        try:
            api_logger.info('Login api initiated with data')

            api_logger.info(request.data)
            return helpers.admin_login_with_password(self, request.data)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())
        
class ResetPasswordApiView(APIView):
    def post(self, request):
        try:
            api_logger.info("reset password api started")
            data = request.data
            return helpers.reset_password(data)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())

class ResetPasswordVerifyApiView(APIView):
    def post(self, request):
        try:
            api_logger.info("reset password verify api started")
            data = request.data
            uid= request.query_params.get('uidb64', '')  # Use request.query_params to get query parameters
            token = request.query_params.get('token', '')
            return helpers.reset_password_verify(data, uid, token)
        except Exception as ex:
            return system_errors.class_exception(ex, self.get_view_name())