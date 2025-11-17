from django.contrib import admin
from django.utils.safestring import mark_safe
from core.models import Vault, VaultType
# Register your models here.

@admin.register(Vault)
class VaultAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created_at',
        'updated_at',
    ]
    list_filter = [
        'vault_type',
        'created_by',
        'shared_team',
        'shared_organization',
    ]
    search_fields = [
        'name'
    ]

    fieldsets = [
        (
            "Data",
            {
                "fields":[
                    ('name',),
                    ('vault_type',),
                    ('username_readonly',),
                    ('password_readonly',),
                    ('url_readonly',),
                ]
            }
        ),
        (
            "Shared",
            {
                "fields":[
                ('shared_team',),
                ('shared_organization',),      
                ]
            }
        ),
        (
            "Details", 
            {
                'fields':[
                        ('value',),
                        ('created_by',),
                    ]
            }
        )
    ]

    readonly_fields=['password_readonly', "url_readonly", "username_readonly"]
    _copy_script_added = False

    def _get_copy_button_html(self, value, field_name):
        """Helper method to generate HTML with copy button"""
        if not value:
            return '-'
        # Escape the value for HTML and JavaScript
        escaped_value = str(value).replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
        button_id = f'copy-btn-{field_name}'
        
        # Add script only once
        script_tag = ''
        if not VaultAdmin._copy_script_added:
            script_tag = '''
        <script>
        if (typeof copyToClipboard === 'undefined') {
            function copyToClipboard(text, buttonId) {
                navigator.clipboard.writeText(text).then(function() {
                    var btn = document.getElementById(buttonId);
                    var originalText = btn.textContent;
                    btn.textContent = 'Copied!';
                    btn.style.backgroundColor = '#28a745';
                    setTimeout(function() {
                        btn.textContent = originalText;
                        btn.style.backgroundColor = '#417690';
                    }, 2000);
                }).catch(function(err) {
                    console.error('Failed to copy: ', err);
                });
            }
        }
        </script>
            '''
            VaultAdmin._copy_script_added = True
        
        html = f'''
        {script_tag}
        <div style="display: flex; align-items: center; gap: 10px;">
            <span id="value-{field_name}" style="flex: 1;">{value}</span>
            <button type="button" id="{button_id}" 
                    onclick="copyToClipboard('{escaped_value}', '{button_id}')"
                    style="padding: 5px 10px; cursor: pointer; background-color: #417690; color: white; border: none; border-radius: 3px;">
                Copy
            </button>
        </div>
        '''
        return mark_safe(html)

    def username_readonly(self, instance):
        value = instance.value.get('username', None)
        if not value:
            value = instance.value.get("email", None)
        return self._get_copy_button_html(value, 'username')
    
    username_readonly.short_description = 'username'

    def url_readonly(self, instance):
        value = instance.value.get('url', None)
        return self._get_copy_button_html(value, 'url')
    
    url_readonly.short_description = 'url'
    
    def password_readonly(self, instance):
        value = instance.value.get('password', None)
        return self._get_copy_button_html(value, 'password')

    password_readonly.short_description = 'password'

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()

@admin.register(VaultType)
class VaultTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    search_fields = [
        'id',
        'name',
    ]