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
from django import forms
from django.utils.translation import ugettext as _


class VideoPostUpdateForm(forms.Form):
    title = forms.CharField(max_length=40, label=_('Title'), required=True)
    description = forms.CharField(label=_('Description'), required=False,  widget=forms.Textarea)
    enabled = forms.BooleanField(label=_('Enabled'), initial=True)
    tags = forms.CharField(label=_('Tags'), required=False)


class VideoPostCreateForm(forms.Form):
    title = forms.CharField(max_length=40, label=_('Title'), required=True)
    description = forms.CharField(label=_('Description'), required=False,  widget=forms.Textarea)
    splash_image = forms.ImageField(label=_('Splash Image'), required=False)
    video = forms.FileField(label=_('Video'), required=True)
    enabled = forms.BooleanField(label=_('Enabled'), initial=True)
    tags = forms.CharField(label=_('Tags'), required=False)
