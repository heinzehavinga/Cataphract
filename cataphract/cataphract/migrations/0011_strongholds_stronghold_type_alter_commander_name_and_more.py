# Generated by Django 5.2 on 2025-05-26 17:24

import django.db.models.deletion
import faker.providers.address
import faker.providers.company
import faker.providers.person
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cataphract', '0010_unittype_base_unit_template_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='strongholds',
            name='stronghold_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cataphract.strongholdtype'),
        ),
        migrations.AlterField(
            model_name='commander',
            name='name',
            field=models.CharField(default=faker.providers.person.Provider.name, max_length=200),
        ),
        migrations.AlterField(
            model_name='detachment',
            name='bio',
            field=models.TextField(blank=True, default=faker.providers.company.Provider.catch_phrase),
        ),
        migrations.AlterField(
            model_name='detachment',
            name='name',
            field=models.CharField(default=faker.providers.company.Provider.company, max_length=200),
        ),
        migrations.AlterField(
            model_name='faction',
            name='name',
            field=models.CharField(default=faker.providers.person.Provider.first_name, max_length=200),
        ),
        migrations.AlterField(
            model_name='hex',
            name='settlement_score',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(default=faker.providers.person.Provider.name, max_length=200),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(default=faker.providers.person.Provider.name, max_length=200),
        ),
        migrations.AlterField(
            model_name='strongholds',
            name='name',
            field=models.CharField(default=faker.providers.address.Provider.city, max_length=200),
        ),
        migrations.AlterField(
            model_name='unittype',
            name='name',
            field=models.CharField(default=faker.providers.person.Provider.first_name, max_length=200),
        ),
    ]
