from django import forms
from django.utils.safestring import mark_safe
from django.utils.dates import WEEKDAYS_ABBR

WEEKDAY_ABBRS = map(lambda t: t[1], sorted(list(WEEKDAYS_ABBR.iteritems())))

class WorkdaysWidget(forms.widgets.NumberInput):

    def render(self, name, value, attrs=None):
        boxes = [ # Create 7 checkboxes, checked for each workday in the week
                """<input type="checkbox" id="bit-{}" {} onChange="update_workdays({});" />""".format(
                    i, 'checked="checked"' if value & (1 << i) else '', i) 
                for i in xrange(7)]
        attrs.update({'type':'hidden'})
        html = super(WorkdaysWidget, self).render(name, value, attrs)
        js = u"""
        <script type="text/javascript">
          function update_workdays(offset) {
              var initial = document.getElementById('id_workdays').value;
              var new_value = initial ^ (1 << offset);
              document.getElementById('id_workdays').value = new_value;
          }
        </script>
        """
        html = u"""
        <div>
            <table>
              <tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>
              <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
            </table>
        """.format(*WEEKDAY_ABBRS+boxes) + html + u"""
        </div>
        """
        return mark_safe(js + html)
