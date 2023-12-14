from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Country, Category


class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ('name', 'iso_code', 'currency', 'flag_img', )

    def flag_img(self, instance):
        img = "<img src='{}'>".format(instance.flag)
        return mark_safe(img)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('title', 'price_per_kilo', 'country', )


admin.site.register(Country, CountryAdmin)
admin.site.register(Category, CategoryAdmin)
