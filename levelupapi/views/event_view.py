"""View module for handling requests about eventEvent types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer


class EventView(ViewSet):
    """Level up eventEvent types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single eventEvent type

        Returns:
            Response -- JSON serialized eventEvent type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all event
        Returns:
            Response -- JSON serialized list of event
        """
        # Make connection with server to retrieve a query set of all event items requested by client and assign the found instances to the event variable

        events = Event.objects.all()
        game = self.request.query_params.get('game')

        if game is not None:
            events = events.filter(game_id=game)
        else:
            pass
        # Set the `joined` property on every event
        for event in events:
            gamer = Gamer.objects.get(user=request.auth.user)
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
        # passes instances stored in event variable to the serializer class to construct data into JSON stringified objects, which it then assigns to variable serializer
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for eventEvent types
    """
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'name', 'date', 'location', 'game')