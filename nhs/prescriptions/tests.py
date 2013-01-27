from django.test import TestCase

from tastypie.test import ResourceTestCase

from models import Product, Prescription

class ProductResourceTest(ResourceTestCase):
    fixtures = ['Product.json',]
    def test_filter_bnf_code(self):
        resp = self.api_client.get('/api/v1/product/?bnf_code__startswith=01', format='json')
        self.assertValidJSONResponse(resp)
        self.assertKeys(self.deserialize(resp), ['meta', 'objects'])
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], 10)
    


class PrescriptionTests(TestCase):
    fixtures = [
        'Product.json', 
        'Prescription.json', 
        'practices/fixtures/Practices.json',
        'ccgs/fixtures/CCG.json'
        ]
    bnf_ids_1 = [
        '0101010R0',
        '0703010F0',
        '0101010G0',
        '0101010P0'
        ]
    bnf_ids_2 = [
        '0703010F0',
        '0101010G0',
        '0101010P0'
        ]

    def test_prescription_aggregate_practice_id(self):
        items = Prescription.objects.compare_codes('practice', self.bnf_ids_1, self.bnf_ids_2)
        self.assertEqual(dict(items), 
            {u'A81016': {'group1': {'items': 1L, 'proportion': 100}, 'group2': {'items': 0, 'proportion': 0}}}
        )

    def test_prescription_aggregate_ccg_id(self):
        items = Prescription.objects.compare_codes('ccg', self.bnf_ids_1, self.bnf_ids_2)
        self.assertEqual(dict(items), 
            {1: {'group1': {'items': 1L, 'proportion': 100}, 'group2': {'items': 0, 'proportion': 0}}}
        )
        
        



