from django.contrib import admin
from .models import Company, Project, Contract
# from django_summernote.widgets import SummernoteWidget


@admin.register(Company)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'business_id']
    # search_fields = ['title', 'body']
    # raw_id_fields = ['author']
    # ordering = ['status', 'publish']
    # formfield_overrides = {
    #     models.TextField: {'widget': SummernoteWidget},
    # }
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Project)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Contract)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'number']
    show_facets = admin.ShowFacets.ALWAYS
