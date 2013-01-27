from django.test import TestCase

from tastypie.test import ResourceTestCase

class ProductResourceTest(ResourceTestCase):
    fixtures = ['Product.json',]
    def test_filter_bnf_code(self):
        resp = self.api_client.get('/api/v1/product/?bnf_code__startswith=01', format='json')
        self.assertValidJSONResponse(resp)
        self.assertKeys(self.deserialize(resp), ['meta', 'objects'])
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], 10)
    


class PrescriptionTests(TestCase):
    fixtures = ['Product.json',]

    def test_prescription_aggregate(self):
        
        bnf_ids_1 = []
        
        



