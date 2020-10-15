# Generated by Django 2.0.6 on 2020-10-15 00:56

from django.db import migrations, models
import django.db.models.expressions
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('appointment_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='appointment_created_by', to='user.User')),
                ('patient', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='appointment_patient', to='user.User')),
                ('physician', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='appointment_physician', to='user.User')),
            ],
            options={
                'db_table': 'appointment',
            },
        ),
    ]
