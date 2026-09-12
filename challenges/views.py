from django.shortcuts import render, get_object_or_404, redirect
from .models import Challenge
from .forms import ChallengeForm

# View que você já criou:
def challenge_list(request):
    challenges = Challenge.objects.filter(is_public=True)
    return render(request, 'challenges/challenge_list.html', {'challenges': challenges})

# NOVA VIEW:
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})


def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            # Atribui provisoriamente o primeiro usuário do banco até implementarmos o login
            from django.contrib.auth.models import User
            challenge.user = User.objects.first()
            challenge.save()
            return redirect('challenge_list')
    else:
        form = ChallengeForm()
    return render(request, 'challenges/challenge_form.html', {'form': form}) 

def home(request):
    return render(request, 'challenges/home.html')
