from django.contrib import admin
from .models import Challenge, Participation

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'target_days', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'description', 'user__username')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'status', 'started_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'challenge__title')

# Troca o texto do topo do painel
admin.site.site_header = "ChallengeHub - Administração"

# Troca o título da aba do navegador
admin.site.site_title = "ChallengeHub Admin"

# Troca o texto da página inicial do admin
admin.site.index_title = "Gerenciamento da Plataforma"
