# This file is part of Bika LIMS
#
# Copyright 2011-2016 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.

from Products.CMFCore.utils import getToolByName
from plone.jsonapi.core import router
from plone.jsonapi.core.interfaces import IRouteProvider
from zExceptions import BadRequest
from zope import interface


class get_index_values(object):
    interface.implements(IRouteProvider)

    def initialize(self, context, request):
        pass

    @property
    def routes(self):
        return (
            ("/get_index_values",
             "get_index_values",
             self.get_index_values,
             dict(methods=['GET', 'POST'])),
        )

    def get_index_values(self, context, request):
        """/@@API/get_index_values: Return all unique contents of
           a catalog index.  This is useful for creating external
           asyc/http vocabularies from Bika LIMS content

        Required parameters:

            - catalog_name: The catalog name
            - index: The role of which users to return

        {
            runtime: Function running time.
            error: true or string(message) if error. false if no error.
            success: true or string(message) if success. false if no success.
            values: A list of values
        }
        
        """
        catalog_name = request.get('catalog_name', None)
        index = request.get('index', None)
        if not all([catalog_name, index]):
            raise BadRequest("catalog_name and index are both required fields.")

        catalog = getToolByName(context, catalog_name, None)
        if not catalog:
            raise BadRequest("catalog not found: '%s'" % catalog_name)

        if index not in catalog.Indexes:
            raise BadRequest("index '%s' not found in '%s'" % (index, catalog_name))

        values = catalog.Indexes[index].uniqueValues()

        ret = {
            "url": router.url_for("get_index_values", force_external=True),
            "success": True,
            "error": False,
            'values': values,
        }
        return ret
