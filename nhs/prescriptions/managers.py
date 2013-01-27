from django.db import models

from collections import defaultdict

class PrescriptionManager(models.Manager):
    def dict_cursor(self, cursor):
        # todo, move somewhere else
        description = [x[0] for x in cursor.description]
        results = []
        for row in cursor:
            results.append(dict(zip(description, row)))
        return results
    
    def bnf_grouped_by_practice_id(self, codes):
        
        codes = "(%s)" % ",".join("'%s'" % c for c in codes)
        
        from django.db import connection
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT practice_id as id, COUNT(*)
            FROM prescriptions_prescription P
            WHERE P.product_id IN %s
            GROUP BY practice_id
            """ % codes)
        
        return self.dict_cursor(cursor)

    def bnf_grouped_by_ccg_id(self, codes):
        
        codes = "(%s)" % ",".join("'%s'" % c for c in codes)
        
        from django.db import connection
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT ccg_id as id, COUNT(*)
            FROM prescriptions_prescription as P
            JOIN practices_practice as PR
            ON P.practice_id = PR.practice
            WHERE P.product_id IN %s
            GROUP BY PR.ccg_id
            """ % codes)
        
        return self.dict_cursor(cursor)
    
    def add_results(self, group, items, key):
        for result in group:
            items[result['id']][key]['items'] = result['count']
        return items
    
    def make_proportions(self, items):
        for k,v, in items.items():
            count_1 = int(v['group1']['items'])
            count_2 = int(v['group2']['items'])
            total = count_1+count_2
            v['group1']['proportion'] = 100 * count_1/total
            v['group2']['proportion'] = 100 * count_2/total
        return items

    def compare_codes(self, query_type, codes1, codes2):
        assert query_type in ('practice', 'ccg')
        if query_type == 'practice':
            group_1 = self.bnf_grouped_by_practice_id(codes1)
            group_2 = self.bnf_grouped_by_practice_id(codes2)

        if query_type == 'ccg':
            group_1 = self.bnf_grouped_by_ccg_id(codes1)
            group_2 = self.bnf_grouped_by_ccg_id(codes2)
        
        def default_dict():
            return {
                        'group1': {'items' : 0, 'proportion': 0},
                        'group2': {'items' : 0, 'proportion': 0}
                    }
        
        items = defaultdict(default_dict)
        
        items = self.add_results(group_1, items, 'group1')
        items = self.add_results(group_2, items, 'group2')
        
        return self.make_proportions(items)


