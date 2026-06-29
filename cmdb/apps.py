from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CmdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cmdb'
    verbose_name = _('CMDB')
