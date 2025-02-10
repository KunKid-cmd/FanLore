from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from ..models import User
from ..forms.profile_edit_view import ProfileUpdateForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for users to update their profile."""
    model = User
    form_class = ProfileUpdateForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        """Return the currently logged-in user."""
        return self.request.user
