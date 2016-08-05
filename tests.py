# p -m unittest discover -s . -b -v

import os
import unittest
import tempfile
from flask import request
import logging

from app import app
from app.logger import logger
from app.utils import check_available_years, get_schema

# logger.setLevel(logging.ERROR)


class UrlsTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_root(self):
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)
    def test_api(self):
        r = self.app.get('/2015/')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/2016/')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/2017/')
        self.assertEqual(r.status_code, 200)

    def test_api_content(self):
        r = self.app.get('/2016/ded320da-058a-4edd-0418-0582389559a7.htm')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/2016/ded320da-058a-4edd-0418-0582389559a7.htm')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/2016/ded320da-058a-4edd-0418-0582389559a7.htm')
        self.assertEqual(r.status_code, 200)

    def test_static(self):
        r = self.app.get('/static/css/bootstrap.css')
        self.assertEqual(r.status_code, 200)

    def test_robot(self):
        r = self.app.get('/robot.txt')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r.mimetype, 'text/html')

    def test_site_map(self):
        rv = self.app.get('/sitemap.xml')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.mimetype, 'application/xml')


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = "514f9d4f-9ef1-2f6d-abe8-c73dcdb1063a.htm"
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_check_available_in(self):
        rv = check_available_years(self.filename)
        self.assertEqual(rv, ['2015','2016','2017'])

    def test_get_schema(self):
        rv = get_schema('2015', self.filename)
        self.assertEqual(rv['name'], 'ACADVersion Enumeration')
        self.assertEqual(rv['description'], 'An enumerated type listing available AutoCAD versions, into which a file may be exported.')
        self.assertEqual(rv['namespace'], 'Autodesk.Revit.DB')
        # rv = check_available_years(filename)
        # self.assertEqual(rv, ['2015','2016','2017'])


if __name__ == '__main__':
    unittest.main()
