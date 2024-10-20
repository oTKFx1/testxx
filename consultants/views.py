from django.shortcuts import render
from django.http import HttpResponse
from . import models
from users.models import NormalUserInfo, SpecialistProfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import serializers
# Create your views here.

# Moyaser API Key:
# Secret_Key: sk_test_qmzkEvYZAo7QWcgbvBk87VJRu3pJu68hoan2KV7s
# Public Key: pk_test_rR95Gy2zwgrqEXcBXpoJpHjkLQL451qW4Vt5g9ii
# Create Payment end-point: https://api.moyasar.com/v1/payments
# Moyaser Note: You can only call this API from the payer device (Browser or Mobile). It is prohibited to call this API from your backend.
# curl 'https://api.moyasar.com/v1/payments' \
# --user 'pk_test_MrtwozLJAuFmLKWWSaRaoaLX:' \
# --header 'Content-Type: application/json' \
# --data '{
 #   "amount": 100,
 #   "currency": "SAR",
#    "description": "Payment for order #",
#    "callback_url": "https://example.com/thankyou",
#    "source": {
#        "type": "creditcard",
#        "name": "Mohammed Ali",
#        "number": "4111111111111111",
#        "cvc": "123",
#        "month": "12",
#        "year": "26"
#    }
#}'

def welcome(request):

    return HttpResponse('Welcome! Consultant')

@api_view(['POST'])
def initiate_consultation(request):
    token = request.data.get('token')
    specialist_id = request.data.get('specialist_id')
    details = request.data.get('details')
    documents = request.FILES.getlist('documents')  # Get the list of uploaded files

    try:
        user = NormalUserInfo.objects.get(token=token)
    except NormalUserInfo.DoesNotExist:
        return Response({'message': 'User Does Not Exist!'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        specialist = SpecialistProfile.objects.get(id=specialist_id)
    except SpecialistProfile.DoesNotExist:
        return Response({'message': 'Specialist Does Not Exist!'}, status=status.HTTP_401_UNAUTHORIZED)

    # Create the ConsultantService instance
    consultant_service = models.ConsultantService(
        user=user,
        details=details,
        specialist=specialist,
    )
    consultant_service.save()  # Save the service instance first

    # Save each document
    for document in documents:
        models.ConsultantDocument.objects.create(service=consultant_service, file=document)

    return Response({'message': 'Consultation initiated successfully!'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def fetch_consultants(request, token):
    try:
        user = NormalUserInfo.objects.get(token=token)
        consultant_services = models.ConsultantService.objects.filter(user=user)
        serializer = serializers.ConsultantServiceSerializer(consultant_services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except NormalUserInfo.DoesNotExist:
        return Response({'message': 'User Does Not Exist!'}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def send_message(request):
    token = request.data.get('token')
    
    # Initialize variables for from_user and to_user
    from_user = None
    to_user = None

    # Check if the user is a NormalUser or Specialist
    try:
        from_user = NormalUserInfo.objects.get(token=token)
        to_user = models.ConsultantService.objects.get(id=request.data.get('consultant_id')).specialist  # Get the specialist
    except NormalUserInfo.DoesNotExist:
        try:
            from_user = SpecialistProfile.objects.get(token=token)
            to_user = models.ConsultantService.objects.get(id=request.data.get('consultant_id')).user.user  # Get the normal user
        except SpecialistProfile.DoesNotExist:
            return Response({'message': 'User Does Not Exist!'}, status=status.HTTP_401_UNAUTHORIZED)

    consultant_id = request.data.get('consultant_id')
    message = request.data.get('message')
    file = request.FILES.get('file')  # Optional

    try:
        consultant_service = models.ConsultantService.objects.get(id=consultant_id)
    except models.ConsultantService.DoesNotExist:
        return Response({'message': 'Consultant Service Does Not Exist!'}, status=status.HTTP_404_NOT_FOUND)

    chat = models.ConsultantChat(
        consultant=consultant_service,
        from_user=from_user.user,  # Adjust based on how you store User in NormalUserInfo and SpecialistProfile
        to_user=to_user,
        message=message,
        file=file
    )
    chat.save()

    return Response({'message': 'Message sent successfully!'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def fetch_messages(request, consultant_id):
    try:
        messages = models.ConsultantChat.objects.filter(consultant_id=consultant_id).order_by('created_at')
        serializer = serializers.ConsultantChatSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except models.ConsultantService.DoesNotExist:
        return Response({'message': 'Consultant Service Does Not Exist!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def complete_consultant(request):
    token = request.data.get('token')
    consultant_id = request.data.get('consultant_id')

    try:
        # Verify specialist by token
        specialist = SpecialistProfile.objects.get(token=token)
    except SpecialistProfile.DoesNotExist:
        return Response({'message': 'Specialist Does Not Exist!'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        consultant_service = models.ConsultantService.objects.get(id=consultant_id, specialist=specialist)
        consultant_service.order_status = 'completed'
        consultant_service.save()
        return Response({'message': 'Consultation completed successfully!'}, status=status.HTTP_200_OK)
    except models.ConsultantService.DoesNotExist:
        return Response({'message': 'Consultant Service Does Not Exist!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def review_specialist(request):
    token = request.data.get('token')
    consultant_id = request.data.get('consultant_id')
    rating = request.data.get('rating')  # Expecting a rating between 0 to 5

    try:
        user = NormalUserInfo.objects.get(token=token)
    except NormalUserInfo.DoesNotExist:
        return Response({'message': 'User Does Not Exist!'}, status=status.HTTP_401_UNAUTHORIZED)

    if rating < 0 or rating > 5:
        return Response({'message': 'Rating must be between 0 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        consultant_service = models.ConsultantService.objects.get(id=consultant_id)
        specialist = consultant_service.specialist  # Get the specialist related to the service

        # Calculate the new average rating
        new_rating_count = specialist.rating_count + 1
        new_average_rating = ((specialist.average_rating * specialist.rating_count) + rating) / new_rating_count
        
        # Update the specialist profile
        specialist.average_rating = new_average_rating
        specialist.rating_count = new_rating_count
        specialist.save()

        return Response({'message': 'Rating submitted successfully!'}, status=status.HTTP_201_CREATED)
    except models.ConsultantService.DoesNotExist:
        return Response({'message': 'Consultant Service Does Not Exist!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def report_consultant(request):
    token = request.data.get('token')
    consultant_id = request.data.get('consultant_id')
    reason = request.data.get('reason')  # Expecting a string reason for reporting

    try:
        user = NormalUserInfo.objects.get(token=token)
    except NormalUserInfo.DoesNotExist:
        return Response({'message': 'User Does Not Exist!'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        consultant_service = models.ConsultantService.objects.get(id=consultant_id)
        # Here you can create a report in a separate model if you have one
        models.Report.objects.create(
            user=user,
            consultant_service=consultant_service,
            reason=reason
        )
        return Response({'message': 'Report submitted successfully!'}, status=status.HTTP_201_CREATED)
    except models.ConsultantService.DoesNotExist:
        return Response({'message': 'Consultant Service Does Not Exist!'}, status=status.HTTP_404_NOT_FOUND)
    






# Handle Payment:
# import json
# import requests
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from .models import ConsultantService
# from django.conf import settings  # For storing API keys securely

# @api_view(['POST'])
# def create_payment(request):
#     # Get necessary details from the request
#     service_id = request.data.get('service_id')
#     consultant_service = ConsultantService.objects.get(id=service_id)

#     # Prepare payment data
#     payment_data = {
#         "amount": 100,  # Adjust this based on your service
#         "currency": "SAR",
#         "description": f"Payment for order #{consultant_service.reference_number}",
#         "callback_url": "https://yourdomain.com/api/payment/callback/",  # Set your callback URL
#         "source": {
#             "type": "creditcard",
#             "name": "Mohammed Ali",
#             "number": "4111111111111111",  # Use actual card details from the frontend
#             "cvc": "123",
#             "month": "12",
#             "year": "26"
#         }
#     }

#     # Call the Moyasar API
#     response = requests.post(
#         'https://api.moyasar.com/v1/payments',
#         auth=(settings.MOYASAR_PUBLIC_KEY, ''),
#         headers={'Content-Type': 'application/json'},
#         data=json.dumps(payment_data)
#     )

#     if response.status_code == 201:  # Check if payment creation was successful
#         payment_info = response.json()
#         # Store the payment info or reference in your database as needed
#         return JsonResponse(payment_info, status=201)
#     else:
#         return JsonResponse(response.json(), status=response.status_code)


# @api_view(['POST'])
# def payment_callback(request):
#     data = request.data

#     # Extract the relevant information from the callback
#     payment_id = data.get('id')
#     status = data.get('status')
    
#     try:
#         # Here, you would typically check the ConsultantService to find the related order
#         consultant_service = ConsultantService.objects.get(reference_number=payment_id)

#         # Update the order status based on the payment status
#         if status == 'succeeded':
#             consultant_service.order_status = 'completed'
#         else:
#             consultant_service.order_status = 'failed'  # Or other statuses as needed
        
#         consultant_service.save()

#         return JsonResponse({'message': 'Status updated successfully!'}, status=200)
    
#     except ConsultantService.DoesNotExist:
#         return JsonResponse({'message': 'Service not found!'}, status=404)


# from .views import create_payment, payment_callback

# urlpatterns = [
#     path('payment/create/', create_payment, name='create_payment'),
#     path('payment/callback/', payment_callback, name='payment_callback'),
# ]