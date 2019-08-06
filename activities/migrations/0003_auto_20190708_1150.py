# Generated by Django 2.2.2 on 2019-07-08 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20190708_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='equipment',
        ),
        migrations.AddField(
            model_name='activity',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.Equipment'),
        ),
        migrations.RemoveField(
            model_name='activity',
            name='space',
        ),
        migrations.AddField(
            model_name='activity',
            name='space',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.Space'),
        ),
    ]