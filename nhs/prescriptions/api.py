from tastypie.resources import ModelResource

from models import Product, Prescription, Group


class ProductResource(ModelResource):
    class Meta:
            model = Product

class PrescriptionResource(ModelResource):
    class Meta:
            model = Prescription

class GroupResource(ModelResource):
    class Meta:
            model = Group


            