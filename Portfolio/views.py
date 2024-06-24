from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from asgiref.sync import sync_to_async
import httpx

class FastAPIView(View):
    async def get(self, request):
        async with httpx.AsyncClient() as client:
            response = await client.get('http://localhost:8000/api/fastapi_endpoint')
            data = response.json()
        return JsonResponse(data)

    async def post(self, request):
        async with httpx.AsyncClient() as client:
            response = await client.post('http://localhost:8000/api/fastapi_endpoint', data={'key': 'value'})
            data = response.json()
        return JsonResponse(data)
