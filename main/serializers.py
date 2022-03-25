from rest_framework import serializers
from .models import Category, Product


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = ('title', 'image', 'url')