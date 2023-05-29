# Generated by Django 4.1.7 on 2023-05-29 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_part_time', models.BooleanField()),
                ('is_full_time', models.BooleanField()),
                ('is_remotable', models.BooleanField()),
                ('is_in_office', models.BooleanField()),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('salary', models.IntegerField()),
                ('experience', models.IntegerField()),
                ('cv_file', models.FileField(blank=True, upload_to=main.models.user_directory_path)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city')),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('experience_min', models.IntegerField()),
                ('experience_max', models.IntegerField()),
                ('is_part_time', models.BooleanField()),
                ('is_full_time', models.BooleanField()),
                ('is_remotable', models.BooleanField()),
                ('is_in_office', models.BooleanField()),
                ('contact_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.employer')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.job')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city')),
            ],
        ),
        migrations.CreateModel(
            name='Seeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField()),
                ('is_from_user', models.BooleanField()),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CVResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.TextField(blank=True, null=True)),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cv')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.offer')),
            ],
        ),
        migrations.AddField(
            model_name='cv',
            name='preferable_job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.job'),
        ),
        migrations.AddField(
            model_name='cv',
            name='seeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.seeker'),
        ),
    ]
