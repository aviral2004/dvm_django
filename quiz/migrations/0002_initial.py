# Generated by Django 4.1.5 on 2023-01-25 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='takenquiz',
            name='taker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken_quizzes', to='users.quiztaker'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz'),
        ),
        migrations.AddField(
            model_name='answered_question',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question'),
        ),
        migrations.AddField(
            model_name='answered_question',
            name='taken_quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.takenquiz'),
        ),
    ]
