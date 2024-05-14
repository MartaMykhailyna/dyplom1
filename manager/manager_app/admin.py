from django.contrib import admin
from .models import *

# admin.site.register(Shoes)
admin.site.register(Users)
admin.site.register(Orders)
admin.site.register(Reservations)

class ShoesImagesAdmin(admin.StackedInline):
    model = ShoesImages

@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    inlines = [ShoesImagesAdmin]
    
    class Meta:
        model = Shoes

@admin.register(ShoesImages)
class ShoesImageAdmin(admin.ModelAdmin):
    pass