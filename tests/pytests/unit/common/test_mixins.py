import pytest
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from main.common.mixins import StaffRequiredMixin
from main.common.test.factories import UserFactory


@pytest.mark.django_db
class TestStaffRequiredMixin:
    class MyView(StaffRequiredMixin, View):
        def get(self, request):
            return HttpResponse('It works', content_type='text/plain')

    @pytest.fixture(autouse=True)
    def setup(self):
        self.view = TestStaffRequiredMixin.MyView()

    def test_allows_staff_member_to_access_the_view(self, rf, admin_user):
        request = rf.get('/')
        request.user = admin_user

        self.view.request = request
        response = self.view.dispatch(request)

        assert response.content == b'It works'

    def test_redirect_to_the_application_root_for_regular_user(self, rf):
        request = rf.get('/')
        request.user = UserFactory.create()

        self.view.request = request
        response = self.view.dispatch(request)

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == '/'

    def test_redirect_to_the_application_root_for_unauthenticated_user(self, rf):
        request = rf.get('/')
        request.user = AnonymousUser()

        self.view.request = request
        response = self.view.dispatch(request)

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == '/'
