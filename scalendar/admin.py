from django.contrib import admin
from scalendar.models import Scalendar, ScalendarException
from scalendar.forms import ScalendarForm

class ScalendarExceptionInline(admin.TabularInline):
    model = ScalendarException

@admin.register(Scalendar)
class ScalendarAdmin(admin.ModelAdmin):
    form = ScalendarForm
    inlines = [ScalendarExceptionInline,]

#admin.site.register(ScalendarException)
