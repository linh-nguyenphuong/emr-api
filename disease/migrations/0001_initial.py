# Generated by Django 2.0.6 on 2020-10-15 16:27

from django.db import migrations, models
import django.db.models.expressions
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('disease_category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=191)),
                ('code', models.CharField(max_length=191, unique=True)),
                ('disease_category', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='disease_category', to='disease_category.DiseaseCategory')),
            ],
            options={
                'db_table': 'disease',
            },
        ),
    ]
