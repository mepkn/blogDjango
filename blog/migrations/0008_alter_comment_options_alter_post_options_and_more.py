# Generated by Django 5.1.5 on 2025-02-24 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_is_public'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-modified_date']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-modified_date']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='date',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='date',
            new_name='created_date',
        ),
        migrations.AddField(
            model_name='comment',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='post',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
