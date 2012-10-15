"""
Serve views for our API callsn
"""
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from nhs.practices.models import Practice
from nhs.prescriptions.models import Product

class ApiView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello beautiful world, I'm not implemented yet, but check back soon!")

def jsonp(fn):
    "Decorator to act as a JSONP API"
    def wrapped(self, request, *args, **kwargs):
        thonic = fn(self, request, *args, **kwargs)

        # Bad request/not found
        if isinstance(thonic, HttpResponse):
            return thonic

        if 'callback' in request.GET:
            return HttpResponse('{0}({1})'.format(request.GET['callback'], json.dumps(thonic)))
        return HttpResponse(json.dumps(thonic), mimetype="application/json")
    return wrapped

class Drug(ApiView):

    @jsonp
    def get(self, request, *args, **kwargs):
        if 'name' not in request.GET:
            return HttpResponseBadRequest("Can't figure out what name you want larry?")
        namestr = request.GET['name']
        if ',' in namestr:
            products = Product.objects.filter(name__in=namestr)
        else:
            products = Product.objects.filter(name__icontains=namestr)
        return [dict(bnf_code=p.bnf_code, name=p.name) for p in products]

class DrugHabits(ApiView):
    pass

class LocalDrug(ApiView):
    pass

class PracticeHabits(ApiView):
    pass

class Practices(ApiView):

    @jsonp
    def get(self, request, *args, **kwargs):
        if 'name' not in request.GET:
            return HttpResponseBadRequest("Can't figure out what name you want larry?")
        namestr = request.GET['name']
        if ',' in namestr:
            practices = Practice.objects.filter(name__in=namestr)
        else:
            practices = Practice.objects.filter(name=namestr)
        return [dict(practice=p.practice, name=p.name,
                     postcode=p.postcode, address=p.address) for p in practices]


