"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Genre


class GenreView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = Genre.objects.all()
        serializer = GenreSerializer(game_types, many=True)
        return Response(serializer.data)

class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Genre
        fields = ('id', 'genre')