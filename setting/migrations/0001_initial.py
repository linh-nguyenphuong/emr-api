# Generated by Django 2.0.6 on 2020-10-15 18:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attribute', models.CharField(max_length=191)),
                ('value', models.CharField(max_length=191)),
            ],
            options={
                'db_table': 'setting',
            },
        ),
    ]
