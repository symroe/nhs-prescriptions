"""
Define the public API for prescriptions
"""
from tastypie.resources import ModelResource, Resource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache

from models import Product, Prescription, Group


class ProductResource(ModelResource):
    class Meta:
            model = Product
            queryset = Product.objects.all()
            filtering = {
                "bnf_code": ALL,
            }
            allowed_methods = ['get']

class PrescriptionResource(ModelResource):
    class Meta:
            model = Prescription
            queryset = Prescription.objects.all()
            allowed_methods = ['get']
            cache = SimpleCache(timeout=1000)

class PrescriptionComparisonResource(ModelResource):
    class Meta:
            model = Prescription
            queryset = Prescription.objects.all()
            filtering = {
                "bnf_code": ALL,
            }
            # This attribute is from my fork of Tastypie Swagger that is
            # yet to be merged upstream - it allows you to specify API
            # documentation details declaratively on the Resource
            custom_filtering = {
                'query_type': {
                    'dataType': 'string',
                    'required': True,
                    'description': 'Granularity of the data you want to retrieve'
                    },
                'group1': {
                    'dataType': 'string',
                    'required': True,
                    'description': 'Frist bucket. Comma separated list of BNF Codes'
                    },
                'group2': {
                    'dataType': 'string',
                    'required': True,
                    'description': 'Second bucket. Comma separated list of BNF Codes'
                    }
                }
            allowed_methods = ['get']

    def apply_filters(self, request):
        # TODO make query_type in to a override_url
        if 'query_type' not in request.GET:
            raise ValueError('Must tell us an aggregation level Larry!')
        query_type = request.GET.get('query_type')
        if 'group1' not in request.GET or 'group2' not in request.GET:
            raise ValueError('Must provide us with buckets!')
        group1 = request.GET.get('group1').split(',')
        group2 = request.GET.get('group2').split(',')
        print group1, group2
        if group2 and group2:
            return Prescription.objects.compare_codes(query_type, group1, group2)

    def get_list(self, request, **kwargs):
        return self.create_response(request, self.apply_filters(request))

class PrescriptionAggregatesResource(ModelResource):
    """
    Provide aggregation data on prescriptions of individual drugs
    """
    class Meta:
        model = Prescription
        queryset = Prescription.objects.all()
        filtering = {
            'bnf_code': ALL
            }
        # Custom documentation
        custom_filtering = {
                'query_type': {
                    'dataType': 'string',
                    'required': True,
                    'description': 'Granularity of the data you want to retrieve'
                    },
                'bnf_code': {
                    'dataType': 'string',
                    'required': True,
                    'description': 'BNF Code you are interested in'
                    }
                }
        allowed_methods = ['get']


    def apply_filters(self, request):
        # TODO make query_type in to a override_url
        if 'query_type' not in request.GET:
            raise ValueError('Must tell us an aggregation level Larry!')
        query_type = request.GET.get('query_type')
        if query_type not in ['ccg', 'practice']:
            raise ValueError('Query type must be one of ccg, practice')
        if 'bnf_code' not in request.GET:
            raise ValueError('Must provide us with a BNF code!')
        bnf_code = request.GET.get('bnf_code')
        meth = getattr(Prescription.objects, 'bnf_grouped_by_{0}_id'.format(query_type))
        print meth, bnf_code
        groups = meth([bnf_code])
        aggs = {x['id']: x for x in groups}
        return dict(objects=aggs)

    def get_list(self, request, **kwargs):
        return self.create_response(request, self.apply_filters(request))


class GroupResource(ModelResource):
    class Meta:
            model = Group
            queryset = Group.objects.all()
            allowed_methods = ['get']
