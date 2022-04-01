from django.contrib import admin

from .models import Review

admin.site.register(Review)

list_display = ('id', 'text', 'author', 'score', 'pub_date',)
search_fields = ('text',)
list_filter = ('pub_date',)
empty_value_display = '-пусто-'
