"""
    Blog model factories
    ====================

    This module defines model factories that can be used to create model instances when preparing
    test data.

"""

import factory
from django.utils.text import slugify
from faker import Factory
from wagtail.core.models import Collection, Page
from wagtail.images import get_image_model

from ..models import (
    ArticlePage, BlogPage, RecipeIngredientsSection, RecipeInstructionsSection, RecipePage,
    SimplePage
)


fake = Factory.create()


class _MP_NodeFactory(factory.DjangoModelFactory):
    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return model_class(**kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = model_class(**kwargs)
        instance._parent_factory = cls
        return instance

    @factory.post_generation
    def parent(self, create, extracted_parent, **parent_kwargs):
        if create:
            parent = self._parent_factory(**parent_kwargs) if parent_kwargs else extracted_parent
            parent.add_child(instance=self) if parent else type(self).add_root(instance=self)
            del self._parent_factory


class _PageFactory(_MP_NodeFactory):
    title = factory.LazyAttribute(lambda o: fake.text(max_nb_chars=50, ext_word_list=None))
    slug = factory.LazyAttribute(lambda o: slugify(o.title))

    class Meta:
        model = Page


class _CollectionFactory(_MP_NodeFactory):
    name = 'Collection'

    class Meta:
        model = Collection


class _CollectionMemberFactory(factory.DjangoModelFactory):
    collection = factory.SubFactory(_CollectionFactory, parent=None)


class _ImageFactory(_CollectionMemberFactory):
    title = 'Image'
    file = factory.django.ImageField()

    class Meta:
        model = get_image_model()


class BlogPageFactory(_PageFactory):
    """ Factory class for the ``BlogPage`` model. """

    class Meta:
        model = BlogPage


class ArticlePageFactory(_PageFactory):
    """ Factory class for the ``ArticlePage`` model. """

    body = factory.LazyAttribute(lambda o: fake.sentences(nb=3, ext_word_list=None))
    header_image = factory.SubFactory(_ImageFactory)

    class Meta:
        model = ArticlePage


class RecipePageFactory(_PageFactory):
    """ Factory class for the ``RecipePage`` model. """

    introduction = factory.LazyAttribute(lambda o: fake.sentences(nb=3, ext_word_list=None))
    header_image = factory.SubFactory(_ImageFactory)
    dish_types = [RecipePage.DISH_TYPE_MAIN_COURSE]

    class Meta:
        model = RecipePage


class SimplePageFactory(_PageFactory):
    """ Factory class for the ``SimplePage`` model. """

    body = factory.LazyAttribute(lambda o: fake.sentences(nb=3, ext_word_list=None))
    header_image = factory.SubFactory(_ImageFactory)

    class Meta:
        model = SimplePage


class RecipeIngredientsSectionFactory(factory.DjangoModelFactory):
    """ Factory class for the ``RecipeIngredientsSection`` model. """

    page = factory.SubFactory(RecipePageFactory)

    class Meta:
        model = RecipeIngredientsSection


class RecipeInstructionsSectionFactory(factory.DjangoModelFactory):
    """ Factory class for the ``RecipeInstructionsSection`` model. """

    page = factory.SubFactory(RecipePageFactory)

    class Meta:
        model = RecipeInstructionsSection
