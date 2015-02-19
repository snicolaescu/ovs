import unittest
import json
from datetime import datetime, timedelta
from app import server

class OVSTest(unittest.TestCase):

    # Template Order
    dueDate = datetime.now() + timedelta(days=6)
    template_order = dict()
    template_order['name'] = 'John Smith'
    template_order['address'] = 'One Verizon Way'
    template_order['city'] = 'Basking Ridge'
    template_order['state'] = 'NJ'
    template_order['zipcode'] = '07920'
    template_order['productType'] = 'SONET'
    template_order['dueDate'] = dueDate.strftime("%m/%d/%Y")

    def setUp(self):
        self.applications = server.test_client()

    def test_root(self):
        result = self.applications.get('/')
        assert 200 == result.status_code
        
    def test_valid_orders(self):
        # Testing productType: SONET
        new_order = self.template_order.copy()
        new_order['productType'] = 'SONET'
        order = json.dumps(new_order)
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 200 == result.status_code

        # Testing productType: FiOS
        new_order = self.template_order.copy()
        new_order['productType'] = 'FiOS'
        order = json.dumps(new_order)
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        # Check Results
        assert 200 == result.status_code

    def test_order_creation(self):
        # Create order
        new_order = self.template_order.copy()
        order = json.dumps(new_order)
        result_post = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result_post = json.loads(result_post.data)
        # Check Results from POST
        assert 200 == result_post.status_code
        # Get the order again via GET
        result_get = self.applications.get('/ovs/orders/' + json_result_post['id'])
        json_result_get = json.loads(result_get.data)
        # Check Results from GET
        assert 200 == result_get.status_code
        assert json_result_post == json_result_get['order']




    ##############################
    # Testing Invalid Scenarios! #
    ##############################

    def test_empty_orders(self):
        # Testing empty order
        order = '{}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'order is empty' == json_result['error']


suite = unittest.TestLoader().loadTestsFromTestCase(OVSTest)
unittest.TextTestRunner(verbosity=2).run(suite)