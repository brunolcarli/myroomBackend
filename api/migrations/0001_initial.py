# Generated by Django 2.2.15 on 2023-09-23 15:04

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(null=True)),
                ('room_picture', models.BinaryField(null=True)),
                ('background_picture', models.BinaryField(null=True)),
                ('default_background_active', models.BooleanField(default=True)),
                ('photos_section_active', models.BooleanField(default=True)),
                ('articles_section_active', models.BooleanField(default=True)),
                ('threads_section_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('avatar', models.BinaryField(null=True)),
                ('full_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ThreadModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_comment_datetime', models.DateTimeField(null=True)),
                ('public', models.BooleanField(default=True)),
                ('num_comments', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserModel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Room')),
            ],
        ),
        migrations.CreateModel(
            name='ThreadComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_datetime', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserModel')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ThreadModel')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.UserModel'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.BinaryField()),
                ('description', models.TextField(blank=True, null=True)),
                ('public', models.BooleanField(default=True)),
                ('post_datetime', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserModel')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('post_datetime', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserModel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Room')),
            ],
        ),
    ]
