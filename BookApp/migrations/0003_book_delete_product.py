# Generated by Django 4.1.7 on 2023-09-10 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0002_product_delete_shoppingcartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('authors', models.CharField(max_length=255)),
                ('publisher', models.CharField(max_length=255)),
                ('publishedDate', models.DateField()),
                ('description', models.TextField()),
                ('pageCount', models.IntegerField()),
                ('categories', models.CharField(max_length=255)),
                ('maturityRating', models.CharField(max_length=255)),
                ('imageLinks', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('previewLink', models.CharField(max_length=255)),
                ('infoLink', models.CharField(max_length=255)),
                ('Genre', models.CharField(max_length=255)),
                ('averageRating', models.FloatField()),
                ('ratingsCount', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
