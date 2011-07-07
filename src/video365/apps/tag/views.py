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
from video365.apps.tag.models import Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from video365.apps.tag.forms import TagForm
from video365.apps.tag.tasks import UpdateTagFilesTask
from video365.helpers.pagination_utils import paginator_numeric
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def admin_index(request, page="1"):
    """
    Loads the Administration panel for the Tags.
    URL: ^admin/tag/$
    """
    variables = dict()
    tag_list = Tag.objects.all()
    max_results = 10
    if tag_list:
        paginator_results, tags = paginator_numeric(tag_list, max_results, page)
        variables.update(paginator_results)
        variables['tags'] = tags.object_list
        variables['pagination_list'] = tags
        variables['title'] = "Tags"
    else:
        messages.warning(request, _('No Results Found.'))
    t = get_template('tag/admin/list.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


@never_cache
@login_required
def create(request):
    """
    Saves a tag.
    URL: ^admin/tag/create/$
    """
    variables = dict()
    variables['title'] = _('Create new Tag')
    if request.POST:
        try:
            tag_form = TagForm(request.POST)
            if tag_form.is_valid():
                name = tag_form.cleaned_data['name']
                tag = Tag()
                tag.name = name
                tag.save()
                messages.success(request, _('Tag successfully created.'))
                return HttpResponseRedirect(reverse(admin_index))
            else:
                messages.warning(request, _('Correct the errors bellow.'))
        except:
            messages.error(request, _('There was an error while saving the Tag.'))
    else:
        tag_form = TagForm()
    variables['tag_form'] = tag_form
    t = get_template('tag/admin/create.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


@never_cache
@login_required
def update(request, tag_id):
    """
    Updates a Tag.
    URL: ^admin/tag/edit/(?P<tag_id>\d+)/$
    """
    variables = dict()
    variables['title'] = _('Edit Tag')
    tag = Tag.objects.get(pk=tag_id)
    if request.POST:
        try:
            tag_form = TagForm(request.POST)
            if tag_form.is_valid():
                name = tag_form.cleaned_data['name']
                tag.name = name
                tag.save()
                messages.success(request, _('Tag successfully updated.'))
                UpdateTagFilesTask.delay()
                return HttpResponseRedirect(reverse(admin_index))
            else:
                messages.warning(request, _('Correct the errors bellow.'))
        except:
            messages.error(request, _('There was an error while saving the Tag.'))
    else:
        tag_form = TagForm(initial={'name': tag.name})
        variables['tag'] = tag
        variables['tag_form'] = tag_form
    t = get_template('tag/admin/update.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


@never_cache
@login_required
def delete(request, tag_id):
    """
    Deletes a Tag.
    URL: ^admin/tag/delete/(?P<tag_id>\d+)/$
    """
    variables = dict()
    tag = Tag.objects.get(pk=tag_id)
    if request.POST:
        try:
            tag.delete()
            UpdateTagFilesTask.delay()            
            messages.success(request, _('Tag successfully deleted.'))
        except:
            messages.error(request, _('There was an error while saving the Tag.'))
        return HttpResponseRedirect(reverse(admin_index))
    else:
        if tag_id is not None:
            variables['tag'] = tag
            t = get_template('tag/admin/delete.html')
            html = t.render(RequestContext(request, variables))
            return HttpResponse(html)
