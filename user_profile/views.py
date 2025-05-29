from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from main.models import Users


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = Users.objects.get(pk=self.request.user.pk)
        return context
