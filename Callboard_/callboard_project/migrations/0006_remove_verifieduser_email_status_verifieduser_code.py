# Generated by Django 4.1.5 on 2023-01-18 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard_project', '0005_verifieduser_alter_category_subscriber_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verifieduser',
            name='email_status',
        ),
        migrations.AddField(
            model_name='verifieduser',
            name='code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
