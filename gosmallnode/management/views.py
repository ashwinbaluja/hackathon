import json
import uuid
import hashlib

from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.serializers import serialize
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
import requests

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
