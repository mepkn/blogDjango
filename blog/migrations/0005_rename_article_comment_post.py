# Generated by Django 5.1.5 on 2025-02-09 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='article',
            new_name='post',
        ),
    ]
