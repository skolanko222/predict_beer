# Generated by Django 4.1.4 on 2022-12-20 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_handling', '0003_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
