from django.shortcuts import render
from django.http import HttpResponse
from .models import Products_updates
import json

# Controller that adds the log row to the log_table
def addLog(request):
    if request.method == 'POST':
        ##get the data
        data = json.loads(request.body)

        ##use the model to insert the row
        row = Products_updates(Updated_at=data['updated_at'][:-6],
                                Product_name=data['title'],
                                Product_description=data['body_html'],
                                Product_id=data['id'])
        row.save()
        return HttpResponse("successfully added row to the logs table",status=201)