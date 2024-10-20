from django.shortcuts import render
from users.models import NormalUserInfo
from . import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
@api_view(['POST'])
def capture_payment(request):
    token = request.data.get('token')
    payment_id = request.data.get('id')  # Get the payment ID from the request
    payment_status = request.data.get('status')  # Get the payment status
    amount = request.data.get('amount')  # Amount in the smallest currency unit
    currency = request.data.get('currency')  # Currency of the payment
    reference_number = request.data.get('source', {}).get('reference_number')  # Get reference number from source
    gateway_id = request.data.get('source', {}).get('gateway_id')  # Get gateway ID from source

    try:
        # Fetch the user based on their email or other means (update this as needed)
        user = NormalUserInfo.objects.get(token=token)  # Update according to your user retrieval logic

        # Create a new Payment instance
        payment = models.Payment(
            user=user,
            amount=amount,
            payment_method='credit_card',  # Assuming payment method from source
            payment_id=payment_id,
            reference_number=reference_number,
            payment_status=payment_status,
            gateway_id=gateway_id,
        )
        payment.save()  # Save the payment instance

        return Response({'message': 'Payment captured successfully!'}, status=status.HTTP_201_CREATED)

    except NormalUserInfo.DoesNotExist:
        return Response({'message': 'User does not exist!'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)