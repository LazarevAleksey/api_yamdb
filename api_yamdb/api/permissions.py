import logging
import sys
from logging import StreamHandler

from rest_framework import permissions

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s__[%(levelname)s]__%(funcName)s__%(lineno)d__%(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class AdminOrReadOnly(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and (
                        request.user.role == 'admin'
                        or
                        (request.get_full_path().split('/')[-2] == 'me' and request.method != 'DELETE')
                    )
        )


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # print(f'user: {request.user}')
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # print(f'request.user.is_user_: {request.user.is_user}')
        res = (request.method in permissions.SAFE_METHODS
            or (request.method == 'PATCH' or 'DELETE'
                                           and (
                                                   obj.author == request.user
                                                   or request.user.role == 'moderator'
                                                   or request.user.role == 'admin')))
        # logger.debug(f'Request: {request.user.is_user} __ {res} ')
        return res
