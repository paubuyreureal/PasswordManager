from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Account


class AccountAdminForm(forms.ModelForm):
    """Custom form that prevents password decryption in admin"""
    
    class Meta:
        model = Account
        fields = ['username', 'url', 'notes', 'icon', 'author']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password_note'] = forms.CharField(
                label='Password',
                widget=forms.TextInput(attrs={'readonly': True}),
                initial='[ENCRYPTED - Only account owner can decrypt]',
                required=False
            )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountAdminForm
    list_display = ['username', 'url', 'author', 'created_at']
    list_filter = ['author', 'created_at']
    search_fields = ['username', 'url']
    readonly_fields = ['created_at']
    
    def get_fieldsets(self, request, obj=None):
        """Customize fieldsets to hide password field"""
        fieldsets = [
            ('Account Information', {
                'fields': ('username', 'url', 'author')
            }),
            ('Additional Information', {
                'fields': ('notes', 'icon', 'created_at'),
                'classes': ('collapse',)
            }),
        ]
        
        if obj:
            fieldsets[0][1]['fields'] = ('username', 'url', 'author', 'password_note')
        
        return fieldsets
    
    def has_change_permission(self, request, obj=None):
        """Allow superusers to modify any account, regular users only their own"""
        if hasattr(request, 'user') and request.user.is_superuser:
            return True
        if obj and hasattr(request, 'user') and request.user != obj.author:
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        """Allow superusers to delete any account, regular users only their own"""
        if hasattr(request, 'user') and request.user.is_superuser:
            return True
        if obj and hasattr(request, 'user') and request.user != obj.author:
            return False
        return super().has_delete_permission(request, obj)
    
    def get_queryset(self, request):
        """Superusers can see all accounts, regular users only their own"""
        qs = super().get_queryset(request)
        if hasattr(request, 'user') and request.user.is_superuser:
            return qs
        if hasattr(request, 'user'):
            return qs.filter(author=request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        """Allow superusers to create accounts for any user, regular users only for themselves"""
        if not change:
            if not hasattr(request, 'user') or not request.user.is_superuser:
                obj.author = request.user
        super().save_model(request, obj, form, change)
