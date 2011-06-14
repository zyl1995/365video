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
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=25, verbose_name=_('Name'), null=False, blank=False)    
    videos_count = 0

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/tag/%i/%s.html" % (self.id, slugify(self.name))

    def get_slug(self):
        return slugify(self.name)
