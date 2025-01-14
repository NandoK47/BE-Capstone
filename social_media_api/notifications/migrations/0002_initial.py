# Generated by Django 5.1.4 on 2025-01-11 22:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notifications', '0001_initial'),
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='user_account.customuser'),
        ),
        migrations.AddField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='user_account.customuser'),
        ),
        migrations.AddField(
            model_name='notification',
            name='target_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
