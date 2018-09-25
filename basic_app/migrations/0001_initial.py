# Generated by Django 2.1.1 on 2018-09-25 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.TextField()),
                ('questiontitle', models.TextField(default='')),
                ('accuracy', models.IntegerField(default=0)),
                ('_submissions', models.IntegerField(default=0)),
                ('all_submissions', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='submissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.TextField()),
                ('qid', models.IntegerField(default=0)),
                ('subtime', models.CharField(default='', max_length=10)),
                ('testCaseScore', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('quest1test', models.IntegerField(default=0)),
                ('quest2test', models.IntegerField(default=0)),
                ('quest3test', models.IntegerField(default=0)),
                ('quest4test', models.IntegerField(default=0)),
                ('quest5test', models.IntegerField(default=0)),
                ('quest6test', models.IntegerField(default=0)),
                ('qflag1', models.BooleanField(default=False)),
                ('qflag2', models.BooleanField(default=False)),
                ('qflag3', models.BooleanField(default=False)),
                ('qflag4', models.BooleanField(default=False)),
                ('qflag5', models.BooleanField(default=False)),
                ('qflag6', models.BooleanField(default=False)),
                ('totalScore', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('attempts', models.IntegerField(default=0)),
                ('question_id', models.IntegerField(default=0)),
                ('phone1', models.CharField(max_length=10)),
                ('phone2', models.CharField(max_length=10)),
                ('name1', models.CharField(max_length=100)),
                ('name2', models.CharField(max_length=100)),
                ('email1', models.EmailField(max_length=254)),
                ('email2', models.EmailField(max_length=254)),
                ('option', models.CharField(default='c', max_length=3)),
                ('level', models.CharField(max_length=10)),
                ('flag', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
