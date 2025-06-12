from rest_framework import serializers
from portfolio.models import Portfolio

class SerializadorPortfolio(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        exclude = []