# Generated by Django 4.2 on 2025-07-24 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название сегмента')),
                ('description', models.TextField(blank=True, verbose_name='Описание сегмента')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID пользователя')),
            ],
        ),
        migrations.CreateModel(
            name='UserSegment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления в сегмент')),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_segments', to='segments.segment', verbose_name='Сегмент')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_segments', to='segments.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Связь пользователя и сегмента',
                'verbose_name_plural': 'Связи пользователей и сегментов',
                'unique_together': {('user', 'segment')},
            },
        ),
    ]
