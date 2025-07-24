from typing import Optional
from django.db import transaction
from segments.models import User, Segment, UserSegment
import random


def create_segment(name: str, description: str = "") -> Segment:
    """
    Создать новый сегмент.
    """
    segment = Segment.objects.create(name=name, description=description)
    return segment


def update_segment(segment_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Segment:
    """
    Обновить данные сегмента.
    """
    segment = Segment.objects.get(id=segment_id)
    if name is not None:
        segment.name = name
    if description is not None:
        segment.description = description
    segment.save()
    return segment


def delete_segment(segment_id: int) -> None:
    """
    Удалить сегмент и все связи с пользователями.
    """
    segment = Segment.objects.get(id=segment_id)
    segment.delete()


def add_user_to_segment(user_id: int, segment_id: int) -> UserSegment:
    """
    Добавить пользователя в сегмент.
    """
    user, _ = User.objects.get_or_create(id=user_id)
    segment = Segment.objects.get(id=segment_id)
    user_segment, _ = UserSegment.objects.get_or_create(user=user, segment=segment)
    return user_segment


def remove_user_from_segment(user_id: int, segment_id: int) -> None:
    """
    Удалить пользователя из сегмента.
    """
    UserSegment.objects.filter(user_id=user_id, segment_id=segment_id).delete()


def assign_segment_to_random_percent_of_users(segment_id: int, percent: float) -> int:
    """
    Случайно распределить сегмент на percent% всех пользователей.
    Возвращает количество добавленных пользователей.
    """
    segment = Segment.objects.get(id=segment_id)
    all_user_ids = list(User.objects.values_list('id', flat=True))
    n = int(len(all_user_ids) * percent / 100)
    selected_user_ids = random.sample(all_user_ids, n) if n > 0 else []
    with transaction.atomic():
        for user_id in selected_user_ids:
            add_user_to_segment(user_id, segment_id)
    return len(selected_user_ids) 