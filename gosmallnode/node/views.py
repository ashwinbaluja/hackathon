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
        selfobj = Self.objects.all()[0].company
        for i in self.companies:
            requests.get("http://" + i.ip + f"/api/preparereceive?token={self.token}&selfname={selfobj.companyName}&selfidentity={selfobj.identity}")

@require_http_methods(["GET"])
def receive_create(request): 
    token = request.GET.get('token')
    print(token, CreationCodes.objects.all())
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

@require_http_methods(["POST"])
def fix_missing(request):
    companylist = json.loads(request.POST['company'])
    if cache.get(request.POST['token']) != None:

        for i in companylist:
            new = Company(**companylist[i])
            new.save()

        return HttpResponse(status_code=200)

    return HttpResponse(status_code=403)

@require_http_methods(["POST"])
def diff_and_create(request):
    companylist = json.loads(request.POST['company'])

    if cache.get(request.POST['token']) != None:

        toadd = []

        for i in Company.objects.all():
            if i.companyName not in companylist:
                toadd.append(i)

        return SendNotifications(HttpResponse(f"[\"{uid}\",{serialize('json', toadd)}]", content_type='application/json'), request.POST['token'], toadd)

@require_http_methods(["GET"])
def get_products(request):
    self = Self.objects.all()
    products = Product.objects.filter(manufacturer=self)

    return HttpResponse(serialize('json', products))

