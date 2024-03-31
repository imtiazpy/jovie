# Generated by Django 5.0 on 2024-03-31 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_type', models.CharField(choices=[('job', 'Job'), ('company', 'Company')], default='job', help_text='Select the type of category', max_length=10)),
                ('title', models.CharField(help_text='The title of the category', max_length=100)),
                ('icon', models.CharField(choices=[('flaticon-accounting', 'Accounting'), ('flaticon-graduation-cap', 'Graduation cap'), ('flaticon-wrench-and-screwdriver-in-cross', 'Wrench and screwdriver'), ('flaticon-consultation', 'Business'), ('flaticon-heart', 'Health'), ('flaticon-computer', 'Computer'), ('flaticon-worker', 'Worker'), ('flaticon-auction', 'Legal'), ('flaticon-user', 'User'), ('flaticon-employee', 'Employee'), ('flaticon-portfolio', 'Portfolio'), ('flaticon-results', 'Results'), ('flaticon-recruitment', 'Recruitment')], default='flaticon-user', help_text='Select the icon you want', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
    ]
