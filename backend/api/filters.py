import django_filters
from django.db.models import Q
from .models import Account


class AccountFilter(django_filters.FilterSet):
    """Custom filter for Account model with advanced filtering options"""
    
    # Text search across multiple fields
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    # Domain filtering (extract domain from URL)
    domain = django_filters.CharFilter(method='filter_domain', label='Domain')
    
    # Date range filtering
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Username filtering
    username_contains = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    
    # URL filtering
    url_contains = django_filters.CharFilter(field_name='url', lookup_expr='icontains')
    
    # Notes filtering
    notes_contains = django_filters.CharFilter(field_name='notes', lookup_expr='icontains')
    
    class Meta:
        model = Account
        fields = ['search', 'domain', 'created_after', 'created_before', 
                 'username_contains', 'url_contains', 'notes_contains']
    
    def filter_search(self, queryset, name, value):
        """Search across username, url, and notes fields"""
        if not value:
            return queryset
            
        return queryset.filter(
            Q(username__icontains=value) |
            Q(url__icontains=value) |
            Q(notes__icontains=value)
        )
    
    def filter_domain(self, queryset, name, value):
        """Filter by domain extracted from URL"""
        if not value:
            return queryset
            
        # Remove protocol if present
        domain = value.lower()
        if domain.startswith(('http://', 'https://')):
            domain = domain.split('://', 1)[1]
        
        # Remove www. if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        # Remove trailing slash
        domain = domain.rstrip('/')
        
        return queryset.filter(
            Q(url__icontains=f'://{domain}') |
            Q(url__icontains=f'://www.{domain}') |
            Q(url__icontains=f'{domain}/')
        )
