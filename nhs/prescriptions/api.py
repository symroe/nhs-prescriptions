from tastypie.resources import ModelResource
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

class GroupResource(ModelResource):
    class Meta:
            model = Group


            