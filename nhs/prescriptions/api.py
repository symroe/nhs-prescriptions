from tastypie.resources import ModelResource, Resource
from tastypie.constants import ALL, ALL_WITH_RELATIONS


from models import Product, Prescription, Group



class ProductResource(ModelResource):
    class Meta:
            model = Product
            queryset = Product.objects.all()
            filtering = {
                "bnf_code": ALL,
            }

class PrescriptionResource(ModelResource):
    class Meta:
            model = Prescription

class PrescriptionComparisonResource(ModelResource):
    class Meta:
            model = Prescription
            queryset = Prescription.objects.all()
            filtering = {
                "bnf_code": ALL,
            }
    def apply_filters(self, request):
        group1 = request.GET.get('group1').split(',')
        group2 = request.GET.get('group2').split(',')
        if group2 and group2:
            return Prescription.objects.compare_codes(group1, group2)
    
    def get_list(self, request, **kwargs):
        return self.create_response(request, self.apply_filters(request))

class GroupResource(ModelResource):
    class Meta:
            model = Group


            