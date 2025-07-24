from django.db import models

class User(models.Model):
    """
    Модель пользователя. В рамках задания храним только ID,
    но можно расширить при необходимости.
    """
    id = models.BigIntegerField(primary_key=True, verbose_name="ID пользователя")

    def __str__(self):
        return f"User {self.id}"

class Segment(models.Model):
    """
    Модель сегмента (экспериментальная группа).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название сегмента")
    description = models.TextField(blank=True, verbose_name="Описание сегмента")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

class UserSegment(models.Model):
    """
    Промежуточная модель для связи пользователей и сегментов (многие-ко-многим).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_segments", verbose_name="Пользователь")
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name="user_segments", verbose_name="Сегмент")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления в сегмент")

    class Meta:
        unique_together = ("user", "segment")
        verbose_name = "Связь пользователя и сегмента"
        verbose_name_plural = "Связи пользователей и сегментов"

    def __str__(self):
        return f"User {self.user_id} in segment {self.segment.name}"
