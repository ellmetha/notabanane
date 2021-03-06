# Generated by Django 2.1.7 on 2019-03-25 02:08

from django.db import migrations, models
import main.common.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepage',
            name='dish_types',
            field=main.common.db.models.fields.ChoiceArrayField(base_field=models.CharField(choices=[('appetizers', 'Appetizers'), ('beverages', 'Beverages'), ('breakfast', 'Breakfast'), ('desserts', 'Desserts'), ('main-course', 'Main course'), ('sauces+salad-dressings', 'Sauces and salad dressings'), ('soups', 'Soups'), ('vegetables+salads', 'Vegetables and salads')], max_length=64), default=list, size=3, verbose_name='Dish types'),
        ),
    ]
