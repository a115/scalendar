scalendar
=========

The reusable app `scalendar` provides calendaring and scheduling functionality for Django. 


Definitions
-----------

We use the term "Scalendar" to refer to a customizable calendar object which holds information about working and non-working days. You can define the general pattern for a work-week (e.g. weekdays and weekend) when you first initialize a Scalendar object. If needed, you can then define various exceptions (e.g. public holidays, working weekends, etc.)

A Scalendar objects has methods that allow you to check whether any given date is a working day or not. 


Working with the Scalendar model
--------------------------------

By default, when you initialize a new `Scalendar` object, it holds a standard western schedule, in which the week begins on Monday, the working days are Monday to Friday, and the weekend is on Saturday and Sunday. No explicit exceptions are defined by default. 

To create a default `Scalendar` object, just give it a name:

    from scalendar.models import Scalendar
    default_scalendar = Scalendar.objects.create(name="My Default Scalendar")

The `workdays` field contains an integer-encoded binary number, where each bit from right to left represents a day of the week, starting from Monday. I.e., the most significant bit of `workdays` is set when Sunday is a working day and the least significant bit is set when Monday is a working day. For example, to check whether Thursday is a workday in our `Scalendar`:

    import calendar
    assert(default_scalendar.workdays & (1 << calendar.THURSDAY) == 8)

There is a (private) helper method that does this:

    assert(default_scalendar._is_workday(calendar.THURSDAY) == True)

To query a specific date, use the `is_workday` or the `is_not_workday` methods:

    from datetime import date
    monday = date(2014, 5, 26)
    assert(default_scalendar.is_workday(monday) == True)
    assert(default_scalendar.is_not_workday(monday) == False)

    saturday = date(2014, 5, 31)
    assert(default_scalendar.is_workday(saturday) == False)
    assert(default_scalendar.is_not_workday(saturday) == True)

You can define a custom Scalendar with a non-standard work-week by passing a binary number for the 'workdays' value to the constructor. For example, to define a work-week in which the weekend is on Friday and Saturday: 

    uae_calendar = Scalendar.objects.create(name="UAE Calendar", int('1001111', 2))

You can now query the custom calendar:

    friday = date(2014, 5, 30)
    assert(uae_calendar.is_workday(friday) == False)
    assert(uae_calendar.is_not_workday(friday) == True)


Scalendar Exception Rules
-------------------------

Individual dates, such as public holidays, can be re-defined in a `Scalendar` by using the `ScalendarException` model. 

    from scalendar.models import Scalendar, ScalendarException
    default_scalendar = Scalendar.objects.create(name="My Default Scalendar")
    christmas_day = date(2014, 12, 25)
    assert(default_scalendar.is_workday(christmas_day) == True) # It's a Thursday
    christmas_exception = ScalendarException.objects.create(calendar=default_calendar, 
                             name="Christmas Day Exception", date=christmas_day, working=False)
    assert(default_scalendar.is_workday(christmas_day) == False)
    assert(default_scalendar.is_not_workday(christmas_day) == True)

You can also, for example, override a specific weekend date to be a workday:

    a_sunday = date(2014, 6, 8)
    assert(default_scalendar.is_workday(a_sunday) == False)
    working_sunday_exception = default_scalendar.exceptions.create(name="Working this Sunday", 
                                   date=a_sunday, working=True)
    assert(default_scalendar.is_workday(a_sunday) == True)

The `ScalendarException` constructor accepts an `end_date` argument for specifying a range of dates for the exception (if not provided, the `end_date` is set to the same value as `date` when the object is saved): 

    start_date = date(2014, 8, 1)
    end_date = date(2014, 8, 31)
    august_vacation = ScalendarException.objects.create(calendar=default_calendar,
                        name="August Vacation", date=start_date, end_date=end_date, 
                        working=False)
    assert(default_scalendar.is_workday(date(2014, 8, 4)) == False)

The behaviour of overlapping exceptions is not defined. 

Recurring exceptions are not yet supported. 
