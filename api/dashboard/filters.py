from base.models import Quote
from base.models import User
from base.models import ApprovedMembers

from django_filters import rest_framework as filters
import django_filters


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username':['iexact','icontains', 'startswith']
        }


class QuoteFilter(filters.FilterSet):
    username = django_filters.CharFilter(field_name='author',lookup_expr='username')
    email = django_filters.CharFilter(field_name='author',lookup_expr='email')
    quote__icontains = django_filters.CharFilter(field_name='quote', lookup_expr='icontains')
    quote__iexact = django_filters.CharFilter(field_name='quote',lookup_expr='iexact')
    release_date_min = django_filters.CharFilter(field_name='created_on',lookup_expr='gte')
    release_date_max = django_filters.CharFilter(field_name='created_on',lookup_expr='lte')
    created_on_date = django_filters.DateFilter(field_name='created_on',lookup_expr='contains')
    signed_by_username = django_filters.CharFilter(field_name='signed', lookup_expr='username')
    signed_by_rank = django_filters.NumberFilter(field_name='signed',lookup_expr='rank')
    signed_by_min_rank = django_filters.NumberFilter(field_name='signed',lookup_expr='rank__gte')
    signed_by_max_rank = django_filters.NumberFilter(field_name='signed',lookup_expr='rank__lte')
    created_on_month = django_filters.NumberFilter(field_name='created_on',lookup_expr='month')
    created_on_year = django_filters.NumberFilter(field_name='created_on',lookup_expr='year')


    class Meta:
        model = Quote
        fields = ('username','author','quote','quote__icontains','quote__iexact','created_on',
                  'release_date_min','release_date_max','signed','signed_by_username'
                  ,'signed_by_min_rank','signed_by_max_rank','created_on_month','created_on_year')


class ApprovedMembersFilter(filters.FilterSet):
    min_rank = django_filters.NumberFilter(field_name='rank',lookup_expr='gt')
    max_rank = django_filters.NumberFilter(field_name='rank',lookup_expr='lt')
    class Meta:
        model = ApprovedMembers
        fields = ('underground_name', 'rank','min_rank','max_rank')