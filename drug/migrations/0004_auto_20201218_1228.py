# Generated by Django 2.0.6 on 2020-12-18 12:28

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('drug_dosage_form', '0001_initial'),
        ('drug_route', '0001_initial'),
        ('drug', '0003_auto_20201028_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='drug_dosage_form',
            field=models.ForeignKey(default='95c5fa9a-7226-407b-af82-22798a0008f1', on_delete=django.db.models.expressions.Case, related_name='drug_drug_dosage_form', to='drug_dosage_form.DrugDosageForm'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drug',
            name='drug_route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.expressions.Case, related_name='drug_drug_route', to='drug_route.DrugRoute'),
        ),
        migrations.AddField(
            model_name='drug',
            name='strength',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
    ]
