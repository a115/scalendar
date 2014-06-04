from django.test import TestCase
from scalendar.widgets import WorkdaysWidget

class WorkdaysWidgetTestCase(TestCase):
    def setUp(self):
        self.widget = WorkdaysWidget()

    def test_widget_renders_corretly(self):
        html = self.widget.render('widget1', 31, {})
        expected_html = """
<script type="text/javascript">
    function update_workdays(offset) {
        var initial = document.getElementById('id_workdays').value;
        var new_value = initial ^ (1 << offset);
        document.getElementById('id_workdays').value = new_value;
    }
</script>

<div>
    <table>
        <tr><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr>
        <tr><td><input type="checkbox" id="bit-0" checked="checked" onChange="update_workdays(0);" /></td><td><input type="checkbox" id="bit-1" checked="checked" onChange="update_workdays(1);" /></td><td><input type="checkbox" id="bit-2" checked="checked" onChange="update_workdays(2);" /></td><td><input type="checkbox" id="bit-3" checked="checked" onChange="update_workdays(3);" /></td><td><input type="checkbox" id="bit-4" checked="checked" onChange="update_workdays(4);" /></td><td><input type="checkbox" id="bit-5"  onChange="update_workdays(5);" /></td><td><input type="checkbox" id="bit-6"  onChange="update_workdays(6);" /></td></tr>
    </table>
    <input name="widget1" type="hidden" value="31" />
</div>
        """
        self.assertHTMLEqual(html.strip(), expected_html)
