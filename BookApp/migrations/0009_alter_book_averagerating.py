# Generated by Django 4.1.7 on 2023-10-03 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0008_alter_book_averagerating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='averageRating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
