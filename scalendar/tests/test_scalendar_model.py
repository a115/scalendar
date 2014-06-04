from django.test import TestCase
from scalendar.models import Scalendar, ScalendarException
from datetime import date
import calendar as cal

class DefaultScalendarTestCase(TestCase):
    def setUp(self):
        s = Scalendar.objects.create(name="Test Default Scalendar")
        self.scalendar_id = s.id

    def test_scalendar_is_properly_created(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertEqual(s.firstweekday, cal.MONDAY, "The first week day should be Monday in the default calendar!")
        self.assertTrue(s._is_workday(cal.MONDAY), "Monday should be a working day!")
        self.assertTrue(s._is_workday(cal.TUESDAY), "Tuesday should be a working day!")
        self.assertTrue(s._is_workday(cal.WEDNESDAY), "Wednesday should be a working day!")
        self.assertTrue(s._is_workday(cal.THURSDAY), "Thursday should be a working day!")
        self.assertTrue(s._is_workday(cal.FRIDAY), "Friday should be a working day!")
        self.assertFalse(s._is_workday(cal.SATURDAY), "Saturday should be a non-working day!")
        self.assertFalse(s._is_workday(cal.SUNDAY), "Sunday should be a non-working day!")

    def test_scalendar_unicode_method_returns_name(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertEqual(unicode(s), u"Test Default Scalendar")

    def test_a_tuesday_is_a_workday(self):
        d = date(2014, 5, 27)
        self.assertEqual(d.weekday(), 1) # If this fails, the world is broken
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertTrue(s.workdays & (1 << d.weekday()))

    def test_a_sunday_is_not_a_workday(self):
        d = date(2014, 6, 1)
        self.assertEqual(d.weekday(), 6) # If this fails, the world is broken
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertFalse(s.workdays & (1 << d.weekday()))

    def test_is_workday_correct_for_a_monday(self):
        d = date(2014, 5, 26)
        self.assertEqual(d.weekday(), 0) # If this fails, the world is broken
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertTrue(s.is_workday(d))
        self.assertFalse(s.is_not_workday(d))

    def test_is_not_workday_correct_for_a_saturday(self):
        d = date(2014, 5, 31)
        self.assertEqual(d.weekday(), 5) # If this fails, the world is broken
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertTrue(s.is_not_workday(d))
        self.assertFalse(s.is_workday(d))

    def test_workweek_repr_returns_correct_string(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertEqual(s.get_week_repr(), u'Monday Tuesday Wednesday Thursday Friday (Saturday) (Sunday)')


class CustomScalendarTestCase(TestCase):
    def setUp(self):
        s = Scalendar.objects.create(name="Custom Scalendar 1", workdays=int('1001111', 2), firstweekday=6)
        self.scalendar_id = s.id

    def test_scalendar_is_properly_created(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertEqual(s.firstweekday, cal.SUNDAY, "The first week day should be Sunday in the default calendar!")
        self.assertTrue(s._is_workday(cal.MONDAY), "Monday should be a working day!")
        self.assertTrue(s._is_workday(cal.TUESDAY), "Tuesday should be a working day!")
        self.assertTrue(s._is_workday(cal.WEDNESDAY), "Wednesday should be a working day!")
        self.assertTrue(s._is_workday(cal.THURSDAY), "Thursday should be a working day!")
        self.assertFalse(s._is_workday(cal.FRIDAY), "Friday should be a non-working day!")
        self.assertFalse(s._is_workday(cal.SATURDAY), "Saturday should be a non-working day!")
        self.assertTrue(s._is_workday(cal.SUNDAY), "Sunday should be a working day!")

    def test_a_sunday_is_a_workday(self):
        d = date(2014, 6, 1)
        self.assertEqual(d.weekday(), 6) # If this fails, the world is broken
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertTrue(s.workdays & (1 << d.weekday()))

    def test_a_saturday_is_not_a_workday(self):
        d = date(2014, 5, 31)
        self.assertEqual(d.weekday(), 5) # If this fails, the world is broken
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertFalse(s.workdays & (1 << d.weekday()))

    def test_is_workday_correct_for_a_monday(self):
        d = date(2014, 5, 26)
        self.assertEqual(d.weekday(), 0) # If this fails, the world is broken
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertTrue(s.is_workday(d))
        self.assertFalse(s.is_not_workday(d))

    def test_is_not_workday_correct_for_a_friday(self):
        d = date(2014, 5, 30)
        self.assertEqual(d.weekday(), 4) # If this fails, the world is broken
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertTrue(s.is_not_workday(d))
        self.assertFalse(s.is_workday(d))
    
    def test_workweek_repr_returns_correct_string(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertEqual(s.get_week_repr(), u'Sunday Monday Tuesday Wednesday Thursday (Friday) (Saturday)')


class ScalendarExceptionsTestCase(TestCase):
    def setUp(self):
        s = Scalendar.objects.create(name="Test Default Scalendar")
        self.scalendar_id = s.id

    def test_exception_is_properly_created(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        d = date(2014, 5, 27)
        e = ScalendarException.objects.create(calendar=s, name="Test Exception", date=d, working=False)
        qs = s.exceptions.all()
        self.assertQuerysetEqual(qs, [repr(e)])
        self.assertEqual(qs[0].name, "Test Exception")

    def test_scalendar_is_workday_respects_exception(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        d = date(2014, 5, 27)
        self.assertTrue(s.is_workday(d))
        e = ScalendarException.objects.create(calendar=s, name="Test Exception", date=d, working=False)
        self.assertFalse(s.is_workday(d))

    def test_scalendar_exception_for_a_weekend_workday(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        d = date(2014, 6, 8)
        self.assertTrue(s.is_not_workday(d)) # It's a Sunday
        e = s.exceptions.create(name="Working this Sunday", date=d, working=True)
        self.assertTrue(s.is_workday(d))

    def test_month_long_scalendar_exception(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        start_date = date(2014, 8, 1) # Friday (workday)
        end_date = date(2014, 8, 31)  # Sunday (weekend)
        self.assertTrue(s.is_workday(start_date))
        self.assertTrue(s.is_workday(date(2014, 8, 4))) # Monday
        self.assertTrue(s.is_not_workday(end_date))
        e = s.exceptions.create(name="August Vacation", date=start_date, end_date=end_date, working=False)
        self.assertTrue(s.is_workday(date(2014, 7, 31))) # Thursday
        for day in range(31):
            vacation_day = date(2014, 8, day+1)
            self.assertFalse(s.is_workday(vacation_day), "This is supposed to be a vacation: {}".format(vacation_day))
        self.assertTrue(s.is_workday(date(2014, 9, 1))) # Monday

    def test_multiple_scalendar_exceptions(self):
        s = Scalendar.objects.get(id=self.scalendar_id)
        self.assertTrue(s.is_workday(date(2014, 5, 26)))
        s.exceptions.create(name="May Bank Holiday", date=date(2014, 5, 26), working=False)
        self.assertFalse(s.is_workday(date(2014, 5, 26)))
        self.assertFalse(s.is_workday(date(2014, 6, 8)))
        s.exceptions.create(name="Working Sunday", date=date(2014, 6, 8), working=True)
        self.assertTrue(s.is_workday(date(2014, 8, 4)))
        s.exceptions.create(name="August Vacation", date=date(2014, 8, 1), end_date=date(2014, 8, 31), working=False)
        self.assertFalse(s.is_workday(date(2014, 8, 4)))
        self.assertTrue(s.is_workday(date(2014, 12, 25)))
        s.exceptions.create(name="Christmas Day", date=date(2014, 12, 25), working=False)
        self.assertTrue(s.is_not_workday(date(2014, 12, 25))) # Christmas Day
        self.assertTrue(s.is_not_workday(date(2014, 8, 4))) # August Vacation
        self.assertTrue(s.is_not_workday(date(2014, 5, 26))) # May Bank Holiday
        self.assertTrue(s.is_workday(date(2014, 6, 8))) # Working Sunday
