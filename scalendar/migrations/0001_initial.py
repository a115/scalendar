# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scalendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('workdays', models.PositiveSmallIntegerField(default=31, verbose_name='work-days')),
                ('firstweekday', models.PositiveSmallIntegerField(default=0, verbose_name='week begins on', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
            ],
            options={
                'verbose_name': 'calendar',
                'verbose_name_plural': 'calendars',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScalendarException',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calendar', models.ForeignKey(to='scalendar.Scalendar', to_field='id', verbose_name='calendar')),
                ('name', models.CharField(max_length=512, verbose_name='exception name')),
                ('date', models.DateField(verbose_name='exception date')),
                ('end_date', models.DateField(null=True, verbose_name='end date', blank=True)),
                ('working', models.BooleanField(default=False, verbose_name='working?')),
            ],
            options={
                'verbose_name': 'calendar exception',
                'verbose_name_plural': 'calendar exceptions',
            },
            bases=(models.Model,),
        ),
    ]
