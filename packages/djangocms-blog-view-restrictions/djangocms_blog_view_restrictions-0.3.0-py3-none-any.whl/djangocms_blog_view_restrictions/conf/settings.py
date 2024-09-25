from django.conf import settings


RAW_ID_FIELDS = getattr(
    settings, "DJANGOCMS_BLOG_VIEW_RESTRICTIONS_RAW_ID_FIELDS", None
)
