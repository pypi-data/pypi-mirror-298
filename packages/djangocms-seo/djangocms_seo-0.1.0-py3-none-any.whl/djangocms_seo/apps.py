from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangocmsSeoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangocms_seo'
    label = 'Django CMS SEO'
    verbose_name = _("Django CMS SEO")
