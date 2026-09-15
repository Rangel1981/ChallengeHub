from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Challenge(models.Model):
    # Relacionamento de 1:N com o criador do desafio
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')

    # Dados do desafio
    title = models.CharField('título', max_length=100)
    description = models.TextField(verbose_name='descrição')

    # Visibilidade: Se True, aparece no feed comunitário. Se False, apenas o dono vê.
    is_public = models.BooleanField('público', default=False)

    # Meta de dias 
    target_days = models.PositiveIntegerField('meta de dias', default=0)

    # Metadados
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

    # Relacionamento de N:N - vários usuários podem participar de vários desafios
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participations')

    # Controle de status
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='iniciado em')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='concluído em')

    class Meta:
        verbose_name = "Participação"
        verbose_name_plural = "Participações"
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} [{self.get_status_display()}]"

    # Retorna o total de check-ins do participante
    def completed_days(self):
        return self.checkins.count()

    # Calcula a porcentagem concluída da meta de dias do desafio
    def progress_percentage(self):
        if self.challenge.target_days <= 0:
            return 0
        percentage = (self.completed_days() / self.challenge.target_days) * 100
        return min(round(percentage), 100)


class CheckIn(models.Model):
    # O check-in pertence a uma participação específica de um usuário no desafio
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='checkins')
    date = models.DateField('data do check-in', default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')

    class Meta:
        verbose_name = "Check-in"
        verbose_name_plural = "Check-ins"
        # Impede mais de 1 check-in do mesmo participante no mesmo dia
        unique_together = ('participation', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Check-in: {self.participation.user.username} em {self.participation.challenge.title} ({self.date})"

class Comment(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField('comentário')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['created_at'] # Ordem cronológica para conversas

    def __str__(self):
        return f"Comentário de {self.user.username} em {self.challenge.title}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications') # Quem recebe
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications') # Quem gerou
    message = models.CharField(max_length=255)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
