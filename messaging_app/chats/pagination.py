from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for the messaging app.
    Returns 20 items per page with the ability to customize page size.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
