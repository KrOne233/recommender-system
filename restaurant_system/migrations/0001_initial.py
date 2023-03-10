# Generated by Django 3.2.9 on 2022-01-30 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurantsystemuser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.CharField(blank=True, max_length=200, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('restaurant', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'restaurantsystemuser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
            ],
        ),
    ]
