from rest_framework import serializers

class AmazonProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.CharField()
    img = serializers.CharField()

class FlipkartProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.CharField()
    img = serializers.CharField()