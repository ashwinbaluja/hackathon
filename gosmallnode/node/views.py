import json
import uuid

from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.serializers import serialize
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
import requests

from .models import Category, Company, CreationCodes, Product, Self

class SendNotifications(HttpResponse):
    def __init__(self, data, token, companies, **kwargs):
        super().__init__(data, **kwargs)
        self.token = token
        self.companies = companies

    def close(self):
        super().close()
        print(self.token)
        selfid = Self.objects.all()
        for i in self.companies:
            requests.get(i.ip + f"/api/preparereceive?token={self.token}&selfname={selfobj.companyName}&selfidentity={selfobj.identity}")

@require_http_methods(["GET"])
def receive_create(request): 
    token = request.GET.get('token')
    if CreationCodes.objects.filter(code=token).exists():
        allCompanies = Company.objects.all()
        uid = str(uuid.uuid4())
        cache.set(uid, 'TRUE', 600)
        CreationCodes.objects.filter(code=token).delete()
        print(uid, allCompanies)
        return SendNotifications(HttpResponse(f"[\"{uid}\",{serialize('json', allCompanies)}]", content_type='application/json'), uid, allCompanies)
    
    return HttpResponseForbidden()

@require_http_methods(["GET"])
def trust_receive(request):
    token = request.GET.get('token')
    if token != None:
        fromobj = Company.objects.filter(name=request.GET.get('selfname'))
        if fromobj.identity == request.GET.get('selfidentity') and fromobj.ip == request.headers['Origin']:
            cache.set(token, 'TRUE', 600)

            return HttpResponse(status_code=200)

    return HttpResponseForbidden()

@require_http_methods(["GET"])
def send_create(request):
    initial = request.GET.get('start')
    token = request.GET.get('token')

    data = requests.get(initial + f"/api/newcompany?token={token}")
    response = data.json()

    myToken = response[0]
    companiesToContact = response[1]

    self = Self.objects.all()
    serializedself = serialize('json', self)
    for i in companiesToContact:
        new = Company(**i)
        new.save()

    postdata = {"companies": companiesToContact, "token": myToken}

    added = False
    additional = {}

    for i in companiesToContact:
        resdata = requests.post(i.ip + "/api/createcompany", data=postdata).json()
        for i in resdata['companies']:
            added = True
            if i not in additional:
                additional[i] = resdata['companies'][i]

    while added == True:
        for i in additional:
            new = Company(**i)
            new.save()

        additional = {}

        added = False
        for x in additional:
            resdata = requests.post(x[ip] + "/api/createcompany", data=postdata).json()
            for i in resdata['companies']:
                added = True
                if i not in additional:
                    additional[i] = resdata['companies'][i]

@require_http_methods(["POST"])
def diff_and_create(request):
    companylist = json.loads(request.POST['company'])

    if cache.get(request.POST['token']) != None:

        toadd = []

        for i in Company.objects.all():
            if i.companyName not in companylist:
                toadd.append(i)

        return SendNotifications(HttpResponse(f"[\"{uid}\",{serialize('json', toadd)}]", content_type='application/json'), request.POST['token'], toadd)

