from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Faq
from .serializers import FaqSerializer

@api_view(['GET', 'POST'])
def faq_list(request):
    if request.method == 'GET':
        faqs = Faq.objects.all()
        serializer = FaqSerializer(faqs, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FaqSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('faq_list')
        return Response(serializer.errors, status=400)
