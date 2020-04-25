"""
    Common mixins
    =============

    This module exposes common mixin classes.

"""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class StaffRequiredMixin(UserPassesTestMixin):
    """ Checks if the logged user is a staff member.

    If the user is not a member of the staff, they are redirected to the root of the application,
    in the other case access is granted.

    """

    def test_func(self):
        """ Returns a boolean indicating whether the current user is a staff member or not. """
        return self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        """ Dispatches the incoming request. """
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
