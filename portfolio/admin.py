from django.contrib import admin
from portfolio.models import Portfolio

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['id', 'freelancer', 'titulo', 'links']
    search_fields = ['titulo', 'freelancer__nome']
    list_filter = ['freelancer']
    
admin.site.register(Portfolio, PortfolioAdmin)