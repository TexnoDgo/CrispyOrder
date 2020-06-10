from django.contrib import admin
# -------------------------------------------------------OLD MODELS----------------------------------------------------
from .models import Order, OperationCategories, Suggestion, AllCity, File, MassOrder
# -------------------------------------------------------OLD MODELS----------------------------------------------------
# -------------------------------------------------------NEW MODELS----------------------------------------------------
from .models import CODCity, CODMaterial, CODCategories, CODOrder, CODDetail, CODFile
# -------------------------------------------------------NEW MODELS----------------------------------------------------

# -------------------------------------------------------OLD MODELS----------------------------------------------------
admin.site.register(Order)
admin.site.register(OperationCategories)
admin.site.register(Suggestion)
admin.site.register(AllCity)
admin.site.register(File)
admin.site.register(MassOrder)
# -------------------------------------------------------OLD MODELS----------------------------------------------------

# -------------------------------------------------------NEW MODELS----------------------------------------------------
admin.site.register(CODCity)
admin.site.register(CODMaterial)
admin.site.register(CODCategories)
admin.site.register(CODOrder)
admin.site.register(CODDetail)
admin.site.register(CODFile)
# -------------------------------------------------------NEW MODELS----------------------------------------------------
