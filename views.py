import json
from re import sub
from wsgiref import headers
from django.http import JsonResponse
import requests
from django.shortcuts import render
from rest_framework.parsers import JSONParser 
from .models import Poll
from .serializers import PollSerializer



subscriptionId= "fc97f7be-f34a-4094-b8fc-fce48e4aad59"
displayName= "azure-cli-2022-02-19-12-20-04"
password="62x2-LWQAxqZTl_RE6a.N1-PPZxQylU9AK"
tenant="248beea9-a793-47c7-abd9-013c00c51146"
client_id="77721f01-75eb-4704-bcbc-e00d38889dcb"


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
    "tenant": "248beea9-a793-47c7-abd9-013c00c51146",
    "Authorization" : "Bearer "+secret,
    "Content-Type" : "application/json"  
    
    }
    response=requests.get(url, headers=headers)
    return render(request,"polls/RG.html",{'response':response.json()},)

def getResource(request):
    secret=getSecret(request)["access_token"]
    
    url= 'https://management.azure.com/subscriptions/fc97f7be-f34a-4094-b8fc-fce48e4aad59/resources?api-version=2021-04-01'
    headers ={
    "tenant": "248beea9-a793-47c7-abd9-013c00c51146",
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
#pass Io17Q~vmoCjmZEG1Q3ND4nWbIq.JH6irQfD9i

def billing(request):
    secret=getSecret(request)["access_token"]
    
    url= 'https://management.azure.com/subscriptions/%s/providers/Microsoft.CostManagement/query?api-version=2021-10-01' %subscriptionId
    headers ={
    "tenant": "248beea9-a793-47c7-abd9-013c00c51146",
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
