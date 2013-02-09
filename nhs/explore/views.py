"""
Views for exploring the dataset dynamically
"""
from django.views.generic import TemplateView

from nhs.prescriptions.models import Product

class Ratio(TemplateView):
    """
    Pick two drugs and get a ratio heatmap
    """
    template_name = 'explore.html'

    def get_context_data(self, **kw):
        context = super(Ratio, self).get_context_data(**kw)
        context['products'] = Product.objects.all()
        return context


class ExploreDrug(TemplateView):
    """
    Explore drugs
    """
    template_name = 'explore_ratio.html'

    def get_context_data(self, **kw):
        context = super(ExploreDrug, self).get_context_data(**kw)
        context['products'] = Product.objects.all()
        return context
