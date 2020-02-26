from calendar import HTMLCalendar
from datetime import datetime, timedelta
from .models import *


class MyCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(MyCalendar, self).__init__()

    def formatday(self, day, events, user):
        events_per_day = events.filter(start__day=day, user=user)
        d = ''
        for event in events_per_day:
            d += f'<li> <a class="{event.urgent}_cal" href="calendar/{event.id}">{event.title} starts @ {event.time_start.strftime("%H:%M")} </a></li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events, user):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, user)
        return f'<tr> {week} </tr>'

    def formatmonth(self,user, withyear=True):
        events = Event.objects.filter(
            start__year=self.year, start__month=self.month, user=user )
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, user)}\n'
        return cal