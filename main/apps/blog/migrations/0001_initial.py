# Generated by Django 2.1.7 on 2019-03-23 03:51

import datetime
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import main.apps.blog.routes
import main.common.db.models.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailimages', '0001_squashed_0021'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.fields.RichTextField(verbose_name='Introduction')),
                ('date', models.DateField(default=datetime.datetime.today, verbose_name='Post date')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', models.CharField(blank=True, help_text='This is the description of your blog', max_length=255, null=True, verbose_name='Description')),
                ('show_tags', models.BooleanField(default=True, verbose_name='Show tags')),
                ('header_image', models.ForeignKey(blank=True, help_text='Default header image used if the featured article does not provide any header image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Header image')),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
            },
            bases=(main.apps.blog.routes.BlogRoutes, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Category name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_set', to='blog.Category', verbose_name='Parent category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CategoryArticlePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.Category', verbose_name='Category')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_categories', to='blog.ArticlePage')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryRecipePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.Category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredientsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label')),
                ('ingredients', models.TextField(help_text='Each new line generates a new numbered ingredient. Blank lines are allowed to separate ingredients from each others too.', verbose_name='Ingredients')),
            ],
            options={
                'verbose_name': 'Recipe ingredients section',
                'verbose_name_plural': 'Recipe ingredients sections',
            },
        ),
        migrations.CreateModel(
            name='RecipeInstructionsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label')),
                ('instructions', models.TextField(help_text='Each new line generates a new numbered instruction. Blank lines are allowed to separate instructions from each others too.', verbose_name='Instructions')),
            ],
            options={
                'verbose_name': 'Recipe instructions section',
                'verbose_name_plural': 'Recipe instructions sections',
            },
        ),
        migrations.CreateModel(
            name='RecipePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.fields.RichTextField(verbose_name='Introduction')),
                ('date', models.DateField(default=datetime.datetime.today, verbose_name='Post date')),
                ('preparation_time', models.DurationField(blank=True, help_text='Duration in the form "HH:MM:SS".', null=True, verbose_name='Preparation time')),
                ('cook_time', models.DurationField(blank=True, help_text='Duration in the form "HH:MM:SS".', null=True, verbose_name='Cook time')),
                ('fridge_time', models.DurationField(blank=True, help_text='Duration in the form "HH:MM:SS".', null=True, verbose_name='Fridge time')),
                ('rest_time', models.DurationField(blank=True, help_text='Duration in the form "HH:MM:SS".', null=True, verbose_name='Rest time')),
                ('recipe_yield', models.CharField(blank=True, help_text='Enter a yield indication such as "4 persons", "3 servings", etc.', max_length=127, verbose_name='Yield')),
                ('dish_types', main.common.db.models.fields.ChoiceArrayField(base_field=models.CharField(choices=[('appetizers', 'Appetizers'), ('beverages', 'Beverages'), ('desserts', 'Desserts'), ('main-course', 'Main course'), ('sauces+salad-dressings', 'Sauces and salad dressings'), ('soups', 'Soups'), ('vegetables+salads', 'Vegetables and salads')], max_length=64), default=list, size=3, verbose_name='Dish types')),
                ('categories', models.ManyToManyField(blank=True, through='blog.CategoryRecipePage', to='blog.Category')),
                ('header_image', models.ForeignKey(blank=True, help_text='Header image displayed when rendering the article or if the article is featured on the home page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Header image')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='TagArticlePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_tags', to='blog.ArticlePage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_tagarticlepage_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TagRecipePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tags', to='blog.RecipePage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_tagrecipepage_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recipepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.TagRecipePage', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='recipeinstructionssection',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructions_sections', to='blog.RecipePage'),
        ),
        migrations.AddField(
            model_name='recipeingredientssection',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_sections', to='blog.RecipePage'),
        ),
        migrations.AddField(
            model_name='categoryrecipepage',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_categories', to='blog.RecipePage'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='categories',
            field=models.ManyToManyField(blank=True, through='blog.CategoryArticlePage', to='blog.Category'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='header_image',
            field=models.ForeignKey(blank=True, help_text='Header image displayed when rendering the article or if the article is featured on the home page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Header image'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.TagArticlePage', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
