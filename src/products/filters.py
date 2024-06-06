from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    """Product filterset"""

    brand = filters.NumberFilter(field_name="brand", lookup_expr="exact")
    category = filters.NumberFilter(
        field_name="category",
        lookup_expr="exact",
        method="filter_category_and_ancestors",
    )

    is_part = filters.BooleanFilter(field_name="is_part", lookup_expr="exact")

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    def filter_category_and_ancestors(self, queryset, name, value):
        try:
            category = Category.objects.get(id=value)
            descendants = category.get_descendants(include_self=True)
            return queryset.filter(category__in=descendants)
        except Category.DoesNotExist:
            return queryset.none()

    class Meta:
        model = Product
        fields = ["category"]
