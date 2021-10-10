from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Provides HTTP status codes

from profiles_api import serializers

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer  # this says, whenever we receive POST, PUT or PATCH, expect to receive a field called name

    # request passed in from Django REST Framework. format used to add format suffix to endpoint URL (not used here but best practice to keep).
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)  # this method is provided by APIView

        # Checks if data is valid in accordance with what we configured in the serializer.
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST  # Note that default is 200 so need to overwrite
            )