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
from ..tag.models import Tag
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _


class VideoPost(models.Model):
    PENDING = 0
    PROCESSING = 1
    READY = 2
    ERROR = 3
    STATE = (
                   (PENDING, _('Pending')),
                   (PROCESSING, _('Processing')),
                   (READY, _('Ready')),
                   (ERROR, _('Error')),
    )

    title = models.CharField(max_length=40, verbose_name=_('Title'), null=False, blank=False)
    description = models.TextField(verbose_name=_('Description'), null=False, blank=False)
    splash_image = models.CharField(max_length=200,  verbose_name=_('Splash Image'), null=True, blank=True)
    video = models.CharField(max_length=200, verbose_name=_('Video'), null=False, blank=False)
    enabled = models.BooleanField(verbose_name=_('Enabled'), default=True)
    publication_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('Tag'), null=True, blank=True)
    locked = models.BooleanField(verbose_name=_('Locked'), default=True)
    state = models.IntegerField(default=0, verbose_name=_('State'), choices=STATE, unique=False, null=False, blank=False)

    class Meta:
        verbose_name = _('Video Post')
        verbose_name_plural = _('Video Posts')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%i/%s.html" % (self.id, slugify(self.title))
