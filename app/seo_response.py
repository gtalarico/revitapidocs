import os

from app import app
from flask import render_template, make_response, redirect, request


@app.route('/robots.txt', methods=["GET"])
def static_from_root():
    path = os.path.join('static', request.path[1:])
    return redirect(path, code=302)
    # return app.send_static_file(os.path.join('static', request.path[1:]))


@app.route("/<int:year>/sitemap.xml", methods=["GET"])
def year_sitemap(year):
    """Generate sitemap.xml """
    pages = ['http://www.revitapidocs.com/',
             'http://www.revitapidocs.com/2015/',
             'http://www.revitapidocs.com/2016/',
             'http://www.revitapidocs.com/2017']
    templates = os.path.join('app', 'templates', str(year))
    for filename in os.listdir(templates):
        url = 'http://www.revitapidocs.com/2015/{}'.format(filename)
        print(filename)
        pages.append(url)

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    """Generate sitemap.xml """
    pages = ['http://www.revitapidocs.com/',
             'http://www.revitapidocs.com/2015/',
             'http://www.revitapidocs.com/2016/',
             'http://www.revitapidocs.com/2017']

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response
