from django.shortcuts import redirect
from django.urls import reverse


def page_not_found(request, exception):
    return redirect(reverse('index'))
