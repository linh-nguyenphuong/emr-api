# Generated by Django 2.0.6 on 2020-10-15 16:17

from django.db import migrations, models
import django.db.models.expressions
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0001_initial'),
        ('emr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmrService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('emr', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='emr_service_emr', to='emr.Emr')),
                ('service', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='emr_service_service', to='service.Service')),
            ],
            options={
                'db_table': 'emr_service',
            },
        ),
    ]
