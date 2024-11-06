from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = '/auth/login'
