from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main:layout_url')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LayoutRender(LoginRequiredMixin, TemplateView):
    template_name = 'main/layout.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_indices'] = range(3)
        return context


class HomePge(LoginRequiredMixin, TemplateView):
    template_name = 'main/home.html'
    login_url = reverse_lazy('login')




