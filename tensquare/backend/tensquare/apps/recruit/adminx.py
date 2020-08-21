import xadmin

from . import models

xadmin.site.register(models.Enterprise)
xadmin.site.register(models.Recruit)
xadmin.site.register(models.City)