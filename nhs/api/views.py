"""
Serve views for our API callsn

Notes:

This approach is distinctly exploratory.
There is code here that could be drier.
On the other hand, when looking at the existing "API-In-A-Box" solutions
out there for Django, they all came up lacking.

Given that the functionality we'd actually use wasn't all that, we're
building our own wheel, and we're going to like it.

Maximum flexibility, and maximum responsiveness to the demands of API
consumers- more important right now than DRY.

Having said that, anyone who wants to try and refactor the generic portions
is welcome:)
"""
import collections
import json

from django.db.models import Sum
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

from nhs.patents.models import Patent
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
        for drug in drugs:
            drughabit = list(sorted(drug.prescription_set.
                                         values('period').
                                         annotate(total=Sum('quantity')),
                                    key=lambda x: x['period']))
            if per:
                for period in drughabit.values():
                    sums[period['period']] += period['quantity']

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
            if 'practice' in request.GET:
                drughabit = list(sorted(drug.prescription_set.
                                        filter(practice__practice = request.GET['practice']).
                                        values('period').
                                        annotate(total=Sum('quantity')),
                                        key=lambda x: x['period']))


            else:
                drughabit = list(sorted(drug.prescription_set.
                                             values('period').
                                             annotate(total=Sum('quantity')),
                                        key=lambda x: x['period']))
            try:
                patent = Patent.objects.get(drug=drug)
                patent = patent.expiry_date.strftime('%Y%m')
            except Patent.DoesNotExist:
                patent = None

            habit.append(dict(code=drug.bnf_code, name=drug.name,
                              patent = patent,
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

    @jsonp
    def get(request):
        if 'name' not in request.GET:
            return HttpResponseBadRequest("Must have a name Larry!")
        practices = nameset(request, Practice)
        habits = []
        # for practice in practices:
        #     scrips = practice.prescription_set.all()
        #     habits.append(
        #         dict(practice=practice.name,
        #              habit={code: d.product.bnf_code,
        #                     period: d.period,
        #                     quantity: d.quantity for d  in scrips})
        #         )
        return habits

def lottery(request):
    g = Group.get(name='lottery')
    drug = g.drugs.all()[0]
    practices = set([p.practice for p in drug.prescription_set.all()])
    render_to_response('examples/lottery.html', dict(practices=practices))
