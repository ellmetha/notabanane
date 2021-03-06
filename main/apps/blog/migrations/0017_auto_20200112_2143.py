# Generated by Django 2.2.9 on 2020-01-13 02:43

from django.db import migrations, models
import main.common.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_recipepage_diets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepage',
            name='diets',
            field=main.common.db.models.fields.ChoiceArrayField(base_field=models.CharField(choices=[('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('gluten+free', 'Gluten free'), ('lactose+free', 'Lactose free')], max_length=12), blank=True, default=list, null=True, size=4, verbose_name='Diets'),
        ),
    ]
