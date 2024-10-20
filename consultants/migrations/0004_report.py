# Generated by Django 5.0.6 on 2024-10-20 04:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultants', '0003_remove_consultantservice_documents_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('consultant_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultants.consultantservice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.normaluserinfo')),
            ],
        ),
    ]
