from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # <-- ADD THIS IMPORT

# Create your views here.
from . models import UserRegistration
from . serializer import RegistrationSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# ... (register_user and list_users functions remain the same) ...

# Apply the decorator here to disable CSRF check for this specific view
@csrf_exempt 
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = UserRegistration.objects.get(pk=pk)
    except UserRegistration.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RegistrationSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RegistrationSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            print("Serizlier errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        # This is the correct status for a successful deletion with no body
        return Response(status=status.HTTP_204_NO_CONTENT)