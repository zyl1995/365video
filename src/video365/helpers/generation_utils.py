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
from django.conf import settings
from django.db import connection
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from video365.helpers.date_utils import get_month_name
import json

def generate_date_menu():
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) AS total, MONTH(publication_date) AS month, YEAR(publication_date) AS year FROM videopost_videopost v WHERE locked = 0 AND enabled = 1 GROUP BY YEAR(publication_date), MONTH(publication_date) ORDER BY year DESC, month')
        line = "<div class='sidebar-module'>"
        line += "<p id='date-sidebar-title' class='sidebar-module-title'>" + _("Archive") + "</p>"
        line += "<div>"
        iteration_year = None
        for row in cursor.fetchall():
            total = row[0]
            month_number = row[1]
            year_number = row[2]
            month_name = get_month_name(month_number)
            if iteration_year != year_number:
                if iteration_year != None:
                    line += "</div>"
                line += "<h3 class='date-sidebar-year date-sidebar-year-collapsed'><a href='#'/>"
                line += str(year_number)
                line += "</a></h3>"
                line += "<div class='month-date-sidebar'>"
                iteration_year = year_number
            line += "<p class='date-sidebar-month'><a href='/date/1/%d/%d/'>" % (year_number, month_number)
            line += "%s (%d)" % (month_name, total)
            line += "</a></p>"
        line += "</div>"
        line += "</div>"
        line += "</div>"
        line = line.encode("utf-8")
        try:
            gendir = '%s/date_menu.inc' % settings.GENERATOR_DIR
            f = open(gendir, "w")
            try:
                f.write(line)
            finally:
                f.close()
        except IOError:
            pass


def generate_tag_files():
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(1), tag_tag.id, tag_tag.name  FROM tag_tag, videopost_videopost, videopost_videopost_tags WHERE videopost_videopost.id = videopost_videopost_tags.videopost_id AND tag_tag.id = videopost_videopost_tags.tag_id AND videopost_videopost.locked = 0 AND videopost_videopost.enabled = 1 GROUP BY tag_tag.id')
    line = "<div class='sidebar-module'>"
    line += "<p id='tag-sidebar-title' class='sidebar-module-title'>" + _("Tags") + "</p>"
    line += "<div>"
    list_tags = []
    for row in cursor.fetchall():
        count = row[0]
        tag_id = row[1]
        tag_name = row[2]
        tag_name_slug = slugify(tag_name)
        line += "<p class='tag-sidebar-item'>"
        line += "<a href='/tag/%d/%s.html'>%s (%d)</a>" % (tag_id, tag_name_slug, tag_name, count)
        line += "</p>"
        list_tags.append(tag_name)
    line += "</div>"
    line += "</div>"
    line2 = "availableTags = "
    line2 += json.dumps(list_tags)    
    line2 += ";"
    line = line.encode("utf-8")
    line2 = line2.encode("utf-8")    
    try:
        gendir = '%s/tag_menu.inc' % settings.GENERATOR_DIR
        gendir2 = '%s/js_tags.inc' % settings.GENERATOR_DIR
        f = open(gendir, "w")
        f2 = open(gendir2, "w")
        try:
            f.write(line)
            f2.write(line2)
        finally:
            f.close()
            f2.close()            
    except IOError:
        pass
