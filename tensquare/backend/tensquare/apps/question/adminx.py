import xadmin

from . import models

xadmin.site.register(models.Label)
xadmin.site.register(models.Question)
xadmin.site.register(models.Reply)