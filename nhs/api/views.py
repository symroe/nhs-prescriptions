"""
Serve views for our API callsn
"""
import json

from django.db.models import Sum
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from nhs.practices.models import Practice
from nhs.prescriptions.models import Group, Product

def nameset(request, model):
    """
    Return the relevant API queryset from the name
    GET param. Allow names to be , delimited.

    Arguments:
    - `request`: Request
    - `model`: Model

    Return: Queryset
    Exceptions: None
    """
    if 'name' not in request.GET:
        return model.objects.all()

    if 'name' in request.GET:
        namestr = request.GET['name']
        if ',' in namestr:
            return model.objects.filter(name__in=namestr)
        else:
            return model.objects.filter(name__icontains=namestr)


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
        products = nameset(request, Product)
        return [dict(bnf_code=p.bnf_code, name=p.name) for p in products]

class DrugHabits(ApiView):
    """
    The historical aggregate of all requested drugs.
    Warning, this will return everything!
    """
    @jsonp
    def get(self, request, *args, **kwargs):
        drugs = nameset(request, Product)
        habit = []
        for drug in drugs:
            drughabit = list(sorted(drug.prescription_set.
                                         values('period').
                                         annotate(total=Sum('quantity')),
                                    key=lambda x: x['period']))

            habit.append(dict(code=drug.bnf_code, name=drug.name,
                              habit=drughabit))

        return habit

class GroupHabits(ApiView):
    """
    The historical aggregate of all drugs
    in the group
    """
    @jsonp
    def get(self, request, *args, **kwargs):
        if 'name' not in request.GET:
            return HttpResponseBadRequest("Must have a name Larry!")
        group = Group.objects.filter(name=request.GET['name'])
        habit = []
        if not group:
            return habit

        for drug in group[0].drugs.all():
            drughabit = list(sorted(drug.prescription_set.
                                         values('period').
                                         annotate(total=Sum('quantity')),
                                    key=lambda x: x['period']))

            habit.append(dict(code=drug.bnf_code, name=drug.name,
                              habit=drughabit))

        return habit



class LocalDrug(ApiView):
    pass

# !!! Extend this to take a location prameter thing
class Practices(ApiView):
    """
    All the information we have on specific practices, or all if
    no specific name is specified.

    example use case: Plot all practices on a map for further drill downs.
    """
    @jsonp
    def get(self, request, *args, **kwargs):
        practices = nameset(request, Practice)
        return [dict(practice=p.practice, name=p.name,
                     postcode=p.postcode, address=p.address) for p in practices]

class PracticeHabits(ApiView):
    pass
