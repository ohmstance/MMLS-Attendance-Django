import bootstrap4
from django.contrib import admin

from .models import Choice, Question

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['question_text', ]}),
        ('Date information',    {'fields': ['pub_date', ]}),
    ]
    inlines = [ChoiceInline, ]
    list_display = ['question_text', 'pub_date', 'was_published_recently', ]
    list_filter = ['pub_date', ]
    search_fields = ['question_text', ]

admin.site.register(Question, QuestionAdmin)
# admin.site.site_header = "Polls administration"
# admin.site.site_title = "Polls site admin"