from django.contrib import admin
from .models import Todoo

@admin.register(Todoo)
class TodooAdmin(admin.ModelAdmin):
    list_display = ('srno', 'title', 'user', 'date', 'status')
    list_filter = ('status', 'date', 'user')
    search_fields = ('title', 'user__username')
