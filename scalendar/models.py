from django.db import models
from django.utils.dates import WEEKDAYS
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

SMALL_INT = models.PositiveSmallIntegerField
WEEKDAY_CHOICES = sorted(WEEKDAYS.iteritems())

class Scalendar(models.Model):
    name = models.CharField(max_length=512, verbose_name=_("name"))
    workdays = SMALL_INT(default=31, verbose_name=_("work-days"))
    firstweekday = SMALL_INT(choices=WEEKDAY_CHOICES, default=0, verbose_name=_("week begins on"))

    class Meta:
        verbose_name = _("calendar")
        verbose_name_plural = _("calendars")

    def __unicode__(self):
        return smart_unicode(self.name)
    
    def _is_workday(self, day_index):
        """ Returns True if the day is set as working day in self.workdays """
        return bool(self.workdays & (1 << day_index))

    def is_workday(self, date_obj):
        """ Given a datetime.date object, returns True if this day is a workday 
        according to the current Scalendar. Otherwise, returns False. """
        result = self._is_workday(date_obj.weekday())
        exceptions = self.exceptions.filter(date__lte=date_obj, end_date__gte=date_obj)
        if exceptions.count():
            result = (exceptions[0].working == True)
        return result
    is_workday.short_description = _("Is a work-day?")

    def is_not_workday(self, date_obj):
        """ Given a datetime.date object, returns False if this day is a workday 
        according to the current Scalendar. Otherwise, returns True. """
        return not self.is_workday(date_obj)
    is_not_workday.short_description = _("Isn't a work-day?")

    def _iter_weekday_indeces(self):
        """ Returns an iterator for the ISO indeces of the days of the week, 
        taking into consideration the self.firstweekday setting. """
        return (((wd + self.firstweekday) % 7) for wd in xrange(7))

    def get_week_repr(self):
        """ Returns a text-based (unicode) representation of the working week 
        defined in this Scalendar. """
        week_repr = []
        for wd in self._iter_weekday_indeces():
            format_str = [u"({})", u"{}"][self._is_workday(wd)]
            week_repr.append(format_str.format(WEEKDAYS[wd]))
        return u" ".join(week_repr)


class ScalendarException(models.Model):
    calendar = models.ForeignKey(Scalendar, related_name='exceptions', verbose_name=_("calendar"))
    name = models.CharField(max_length=512, verbose_name=_("exception name"))
    date = models.DateField(verbose_name=_("exception date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    working = models.BooleanField(default=False, verbose_name=_("working?"))

    class Meta:
        verbose_name = _("calendar exception")
        verbose_name_plural = _("calendar exceptions")

    def save(self, *args, **kwargs):
        if (not self.end_date) or (self.end_date < self.date):
            self.end_date = self.date
        super(ScalendarException, self).save(*args, **kwargs)
