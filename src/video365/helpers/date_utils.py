# -*- coding: utf-8 -*-
'''
Copyright Cobalys.com (c) 2011

This file is part of 365Video.

    365Video is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    365Video is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with 365Video.  If not, see <http://www.gnu.org/licenses/>.
'''
from django.utils.translation import ugettext as _
import datetime

def get_month_name(month):
    month_names = {
                        1: _('January'),
                        2: _('February'),
                        3: _('March'),
                        4: _('April'),
                        5: _('May'),
                        6: _('June'),
                        7: _('July'),
                        8: _('August'),
                        9: _('September'),
                        10: _('October'),
                        11: _('November'),
                        12: _('December'),
                    }
    return month_names[month]

def get_day_name(year, month, day):
    day_names = {
                    0: _('Monday'),
                    1: _('Tuesday'),
                    2: _('Wednesday'),
                    3: _('Thursday'),
                    4: _('Friday'),
                    5: _('Saturday'),
                    6: _('Sunday'),
                }
    day_week = datetime.date(year, month, day).weekday()
    return day_names[day_week]
