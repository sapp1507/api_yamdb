from django_filters import AllValuesFilter, CharFilter, FilterSet

from reviews.models import Title


class TitleFilterSet(FilterSet):
    genre = CharFilter(field_name='genre', lookup_expr='slug')
    category = CharFilter(field_name='category', lookup_expr='slug')
    year = AllValuesFilter(field_name='year')
    name = AllValuesFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'genre', 'category'
        )
