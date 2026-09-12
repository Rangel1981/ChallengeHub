from django.shortcuts import render, get_object_or_404
from .models import Challenge

# View que você já criou:
def challenge_list(request):
    challenges = Challenge.objects.filter(is_public=True)
    return render(request, 'challenges/challenge_list.html', {'challenges': challenges})

# NOVA VIEW:
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})
