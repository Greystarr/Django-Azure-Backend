import json
from re import sub
from wsgiref import headers
from django.http import JsonResponse
import requests
from django.shortcuts import render
from rest_framework.parsers import JSONParser 
from .models import Poll
from .serializers import PollSerializer



subscriptionId= "fXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
displayName= "azure-cliXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
password="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
tenant="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
client_id="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


def index(request):
    return render(request, "polls/index.html")
def poll_list(request):
    if request.method == 'GET':
        polls= Poll.objects.all()
        serializer= PollSerializer(polls,many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PollSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

def getRG(request):
    secret=getSecret(request)["access_token"]
    
    url= 'https://management.azure.com/subscriptions/%s/resourcegroups?api-version=2021-04-01' %subscriptionId
    headers ={
    "tenant": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "Authorization" : "Bearer "+secret,
    "Content-Type" : "application/json"  
    
    }
    response=requests.get(url, headers=headers)
    return render(request,"polls/RG.html",{'response':response.json()},)

def getResource(request):
    secret=getSecret(request)["access_token"]
    
    url= 'https://management.azure.com/subscriptions/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/resources?api-version=2021-04-01'
    headers ={
    "tenant": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "Authorization" : "Bearer "+secret,
    "Content-Type" : "application/json"  
    
    }
    response=requests.get(url, headers=headers)
    return render(request,"polls/resource.html",{'response':response.json()},)

    

def getSecret(request):
    data={
    'grant_type':'client_credentials',
    'client_id': client_id,
    'client_secret' : password,
    'resource' : 'https://management.azure.com'
    }
    response=requests.post('https://login.microsoftonline.com/'+tenant+'/oauth2/token', data=data)
    return (response.json())

def billing(request):
    secret=getSecret(request)["access_token"]
    
    url= 'https://management.azure.com/subscriptions/%s/providers/Microsoft.CostManagement/query?api-version=2021-10-01' %subscriptionId
    headers ={
    "tenant": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "Authorization" : "Bearer "+secret,
    "Content-Type" : "application/json"  
    
    }
    data={
  "type": "Usage",
  "timeframe": "TheLastMonth",
  "dataset": {
    "granularity": "None",
    "aggregation": {
      "totalCost": {
        "name": "PreTaxCost",
        "function": "Sum"
      }
    },
    "grouping": [
      {
        "type": "Dimension",
        "name": "ResourceGroup"
      }
    ]
  }
}

    response=requests.post(url, headers=headers, json=data)
    respJson=response.json()
    info=respJson["properties"]["rows"]
    sum=0
    for i in info:
        sum=sum+i[0]
    return render(request,"polls/billing.html",{'response':info,'sum':sum},)
