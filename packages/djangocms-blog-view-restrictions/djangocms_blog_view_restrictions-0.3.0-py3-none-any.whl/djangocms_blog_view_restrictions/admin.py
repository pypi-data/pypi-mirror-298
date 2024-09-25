from django.contrib import admin
from django.utils.translation import gettext as _
import djangocms_blog.admin as blog_admin

from .conf import settings as local_settings
from .models import ViewRestrictionExtension


class ViewRestrictionExtensionInline(admin.TabularInline):
    model = ViewRestrictionExtension
    fields = ["post", "user", "group"]
    classes = ["collapse"]
    can_delete = True
    extra = 1
    verbose_name = _("View restriction")
    verbose_name_plural = _("View restrictions")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if local_settings.RAW_ID_FIELDS is not None:
            self.raw_id_fields = local_settings.RAW_ID_FIELDS


blog_admin.register_extension(ViewRestrictionExtensionInline)
