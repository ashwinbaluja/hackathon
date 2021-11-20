import hashlib
import json
import time
import uuid

import requests
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.core.serializers import serialize
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from node.models import Category, Company, CreationCodes, Product, Self


@require_http_methods(["GET"])
def create_self(request):
    name = request.GET['name']
    ip = request.GET['ip']
    tohash = name + ip
    hashed = hashlib.md5(tohash)
    fromobj = Category.objects.filter(categoryName=request.GET['category'])

    newcompany = Company(companyName=name, companyCategory=fromobj, ip=ip, identity=hashed.hexdigest())
    newcompany.save()

    self = Company(company=newcompany)
    self.save()

@require_http_methods(["POST"])
def create_product(request):
    uploaded_file = File(request.FILES['file'])
    filename = str(time.time()).split(".")[0] + ".png"
    uploaded_file.save('productfiles', f.readlines(), True)
    self = Self.objects.all()[0].company
    new = Product(productImage=self.ip + "/static/" + filename, productName=request.POST['name'], productTags=request.POST['tags'], manufacturer=self)
    new.save()
    
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
    totaladditional = {}

    for i in companiesToContact:
        resdata = requests.post(i.ip + "/api/createcompany", data=postdata).json()
        for i in resdata['companies']:
            added = True
            if i not in additional:
                additional[i] = resdata['companies'][i]

            if i not in totaladditional:
                totaladditional[i] = resdata['companies'][i]

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

                if i not in totaladditional:
                    totaladditional[i] = resdata['companies'][i]

    data = {"token": myToken, "companies": serialize('json', totaladditional)}
    requests.post(initial + "/api/missing/", data=data)

    selfCategory = self.companyCategory
    sameCategory = Company.objects.filter(companyCategory=selfCategory)

    for i in sameCategory: 
        products = requests.get(i.ip + "/api/products/").json()
        for x in products:
            new = Product(**x)
            new.save()



