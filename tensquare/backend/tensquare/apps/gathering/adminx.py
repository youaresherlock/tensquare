import xadmin
from xadmin import views

from . import models


xadmin.site.register(models.Gathering)