from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict
from django.conf import settings




class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 20
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('lastPage', self.page.paginator.num_pages),
            ('countItemsOnPage', self.get_page_size(self.request)),
            ('current', self.page.number),
            ('next', self.page.next_page_number() if self.page.has_next() else None),
            ('previous', self.page.previous_page_number() if self.page.has_previous() else None),
            ('results', data)
        ]))

def get_settings():
    return  {}