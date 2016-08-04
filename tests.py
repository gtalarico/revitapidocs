# p -m unittest discover -s . -b -v

import os
import unittest
import tempfile
from flask import request
import logging

from app import app
from app.logger import logger

logger.setLevel(logging.ERROR)


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_root(self):
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)
        # import ipdb; ipdb.set_trace()

        # with app.test_request_context('/'):
            # print('>>>',request.status)

    # def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
