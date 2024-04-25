from rest_framework import serializers
from .models import Watch

class WatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch
        fields = ['id', 'brand', 'name', 'description', 'more_description', 'rating', 'price', 'year']
