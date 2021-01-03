from django.contrib import admin

# Register your models here.
from .models import Group, Tag, Product


class TagInline(admin.TabularInline):
    model = Tag
    extra = 3


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3


class GroupAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name']})]
    inlines = [ProductInline]


#class ProductAdmin(admin.ModelAdmin):
#    fieldsets = [(None, {'fields': ['content']})]
#    inlines = [TagInline]


admin.site.register(Tag)
admin.site.register(Group, GroupAdmin)
admin.site.register(Product) #, ProductAdmin)
