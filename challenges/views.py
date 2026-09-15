from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Challenge, CheckIn, Comment, Notification, Participation
from .forms import ChallengeForm, CustomUserCreationForm
import re

# --- VIEWS DA APLICAÇÃO ---

def home(request):
    return render(request, 'challenges/home.html')

def challenge_list(request):
    challenges = Challenge.objects.filter(is_public=True)
    return render(request, 'challenges/challenge_list.html', {'challenges': challenges})

def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    # Filtre apenas os comentários principais (parent=None)
    comments = challenge.comments.filter(parent__isnull=True).order_by('-created_at')
    return render(request, 'challenges/challenge_detail.html', {
        'challenge': challenge,
        'comments': comments,
    })
@login_required(login_url='login')
def challenge_create(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.user = request.user
            challenge.save()
            return redirect('challenge_list')
    else:
        form = ChallengeForm()
    return render(request, 'challenges/challenge_form.html', {'form': form})

# --- VIEWS DE AUTENTICAÇÃO E CONFIRMAÇÃO ---

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Conta inativa até confirmar o e-mail
            user.save()

            # Gerar Token e UID seguros
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Link de ativação
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            # Enviar e-mail (Impresso no Terminal)
            subject = "Confirme seu e-mail - ChallengeHub"
            message = f"Olá {user.first_name},\n\nObrigado por se cadastrar no ChallengeHub! Clique no link abaixo para ativar sua conta:\n\n{activation_link}\n\nSe você não solicitou este cadastro, ignore este e-mail."
            
            send_mail(subject, message, 'noreply@challengehub.com', [user.email])

            messages.info(request, 'Cadastro realizado! Verifique seu e-mail (no console) para ativar a conta.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'challenges/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Sua conta foi ativada com sucesso!')
        return redirect('challenge_list')
    else:
        messages.error(request, 'O link de ativação é inválido ou já expirou.')
        return redirect('home')


def login_view(request):    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'challenges/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    user_challenges = Challenge.objects.filter(user=request.user)
    return render(request, 'challenges/dashboard.html', {'challenges': user_challenges})


def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    participation = None
    has_checked_in_today = False

    if request.user.is_authenticated:
        participation = Participation.objects.filter(user=request.user, challenge=challenge).first()
        if participation:
            has_checked_in_today = participation.checkins.filter(date=timezone.now().date()).exists()

    # Busca apenas os comentários raiz (as respostas vêm através de comment.replies.all)
    comments = challenge.comments.filter(parent=None).select_related('user').prefetch_related('replies__user')

    context = {
        'challenge': challenge,
        'participation': participation,
        'has_checked_in_today': has_checked_in_today,
        'comments': comments,
    }
    return render(request, 'challenges/challenge_detail.html', context)


@login_required(login_url='login')
def checkin_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    # Busca ou cria a participação do usuário ao tentar fazer o check-in
    participation, _ = Participation.objects.get_or_create(
        user=request.user,
        challenge=challenge
    )

    today = timezone.now().date()
    
    # Registra o check-in na participação do usuário
    checkin, created = CheckIn.objects.get_or_create(
        participation=participation, 
        date=today
    )
    
    if created:
        messages.success(request, 'Check-in realizado com sucesso! Mandou bem! 🔥')
    else:
        messages.info(request, 'Você já fez o check-in de hoje neste desafio.')

    return redirect('challenge_detail', challenge_id=challenge.id)

@login_required(login_url='login')
def feed(request):
    # Busca os últimos check-ins públicos para a linha do tempo
    latest_checkins = CheckIn.objects.filter(
        participation__challenge__is_public=True
    ).select_related('participation__user', 'participation__challenge')[:20]

    # Busca os novos desafios públicos criados recentemente
    recent_challenges = Challenge.objects.filter(
        is_public=True
    ).select_related('user')[:5]

    context = {
        'checkins': latest_checkins,
        'recent_challenges': recent_challenges,
    }
    return render(request, 'challenges/feed.html', context)

def add_comment(request, challenge_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        parent_obj = None
        if parent_id:
            parent_obj = Comment.objects.filter(id=parent_id).first()

        Comment.objects.create(
            challenge_id=challenge_id,
            user=request.user,  
            content=content,
            parent=parent_obj
        )

    return redirect('challenge_detail', challenge_id)


# View para marcar todas as notificações como lidas
@login_required(login_url='login')
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'home'))
