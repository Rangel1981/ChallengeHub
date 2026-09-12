from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
#relacionamento de 1:N
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')

#dados do desafio
    title = models.CharField('titulo', max_length=100)
    description = models.TextField(verbose_name='descricao')

# Visibilidade: Se True, aparece no feed comunitário. Se False, apenas o dono vê.
    is_public = models.BooleanField('publico', default=False)

#meta de dias 
    target_days = models.PositiveIntegerField('meta de dias', default=0)

#metadados
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    class Meta:
        verbose_name = "Desafio"
        verbose_name_plural = "Desafios"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} (por {self.user.username})"

class Participation(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('abandoned', 'Abandonado'),
    ]

# relacionamento de N:N - varios usuarios podem participar de varios desafios
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participations')

#controle de status
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='iniciado em')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='concluido em')

    class Meta:
        verbose_name = "Participação"
        verbose_name_plural = "Participações"
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} [{self.get_status_display()}]"

