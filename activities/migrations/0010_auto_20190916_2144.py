# Generated by Django 2.2.2 on 2019-09-17 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_auto_20190916_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.RemoveField(
            model_name='activity',
            name='space',
        ),
        migrations.AddField(
            model_name='activity',
            name='space',
            field=models.ManyToManyField(blank=True, null=True, to='activities.Space'),
        ),
    ]