from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, 'frontend/index.html')


@login_required
def game_detail(request, game_id):
    return render(request,
                  'frontend/game_detail.html',
                  context={'game_id': game_id})
