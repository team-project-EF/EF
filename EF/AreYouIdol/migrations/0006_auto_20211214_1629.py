# Generated by Django 3.2.9 on 2021-12-14 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AreYouIdol', '0005_auto_20211214_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.DeleteModel(
            name='ImageUpload',
        ),
    ]
