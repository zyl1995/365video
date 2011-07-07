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
from video365.apps.videopost.models import VideoPost
from video365.apps.tag.models import Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from video365.apps.videopost.forms import VideoPostCreateForm, \
    VideoPostUpdateForm
from video365.apps.videopost.tasks import CreateVideopostTask, \
    DeleteAsociatedFilesTask, DeleteVideopostTask, EditVideopostTask
from video365.helpers.date_utils import get_day_name, get_month_name
from video365.helpers.pagination_utils import paginator_simple, \
    paginator_numeric
import datetime
import settings


def retrieve(request, videopost_id):
    """
    Gets one Video Post
    """
    variables = dict()
    videopost_id = int(videopost_id)
    videopost = get_object_or_404(VideoPost, pk=videopost_id, enabled=True, locked=False)
    variables['videopost'] = videopost
    variables['title'] = videopost.title
    t = get_template('videopost/retrieve.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


def retrieve_all(request, page=1):
    """
    Gets All the Video Post
    URL: ^(?P<page>\d+)/$
    """
    variables = dict()
    max_results = 5
    previous_page = int(page) - 1
    next_page = int(page) + 1
    videopost_list = VideoPost.objects.filter(enabled=True, locked=False).order_by('-publication_date')
    if videopost_list:
        videoposts_paginated = paginator_simple(videopost_list, max_results, page)
        variables['videoposts'] = videoposts_paginated
        variables['previous-page-link'] = "%d/" % previous_page
        variables['next-page-link'] = "%d/" % next_page
    else:
        messages.info(request, _('No Results Found.'))
    t = get_template('videopost/list.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


def get_by_date(request, page, year, month=None, day=None):
    """
    Gets All the Video Post by Date.
    URL: ^date/(?P<page>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$
         ^date/(?P<page>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/$
         ^date/(?P<page>\d+)/(?P<year>\d{4})/$
    """
    variables = dict()
    page = int(page)
    previous_page = page - 1
    next_page = page + 1
    max_results = 5
    if year.isdigit():
        year = int(year)
    else:
        return HttpResponse(status=400)
    headline = _('Showing result for %(year)s.') % {'year': year}
    previous_page_link = "date/%d/%d/" % (previous_page, year)
    next_page_link = "date/%d/%d/" % (next_page, year)
    videopost_list = VideoPost.objects.filter(enabled=True, locked=False)
    videopost_list = videopost_list.filter(publication_date__year=year).order_by('-publication_date')
    if month and month.isdigit():
        month = int(month)
        month_name = get_month_name(month)
        videopost_list = videopost_list.filter(publication_date__month=month)
        previous_page_link = previous_page_link + str(month) + "/"
        next_page_link = next_page_link + str(month) + "/"
        headline = _('Showing result for: %(month)s %(year)d.') % {'month': month_name, 'year': year}
        if day and day.isdigit():
            day = int(day)
            day_name = get_day_name(day)       
            videopost_list = videopost_list.filter(publication_date__day=day)
            previous_page_link = previous_page_link + str(day) + "/"
            next_page_link = next_page_link + str(day) + "/"
            headline = _('Showing result for: %(day)s %(month)s %(year)d.') % {'day': day_name, 'month': month_name, 'year': year}
    if videopost_list:            
        videoposts_paginated = paginator_simple(videopost_list, max_results, page)
        variables['videoposts'] = videoposts_paginated
        variables['headline'] = headline 
        variables['previous-page-link'] = "%d/" % previous_page
        variables['next-page-link'] = "%d/" % next_page
    else:
        messages.info(request, _('No Results Found.'))
    t = get_template('videopost/list.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


def get_by_tag(request, tag_id, page=1):
    """
    Gets All the Video Post by Tag.
    URL: ^tag/(?P<tag_id>\d+)/(?P<page>\d+)/([\w-]+).html$
         ^tag/(?P<tag_id>\d+)/([\w-]+).html$
    """
    variables = dict()
    max_results = 5
    previous_page = page - 1
    next_page = page + 1
    tag_id = int(tag_id)
    tag = get_object_or_404(Tag, pk=tag_id)
    variables['tag'] = tag
    videopost_list = tag.videopost_set.filter(enabled=True, locked=False).order_by('-publication_date')
    if videopost_list:
        videoposts_paginated = paginator_simple(videopost_list, max_results, page)
        variables['videoposts'] = videoposts_paginated
        headline = _('Showing result for: %(tag)s.') % {'tag': tag.name}
        variables['headline'] = headline                 
        variables['previous-page-link'] = "tag/%d/%d/%s.html" % (tag_id, previous_page, tag.get_slug())
        variables['next-page-link'] = "tag/%d/%d/%s.html" % (tag_id, next_page, tag.get_slug())
    else:
        messages.info(request, _('No Results Found.'))
    t = get_template('videopost/list.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


@never_cache
@login_required
def create(request):
    """
    Creates a new Video Post.
    """
    variables = dict()
    videopost_id = 0
    variables['title'] = _('Create new Video Post.')
    if request.POST:
        video_form = VideoPostCreateForm(request.POST, request.FILES)
        if video_form.is_valid():
            try:
                title = video_form.cleaned_data['title']
                description = video_form.cleaned_data['description']
                enabled = video_form.cleaned_data['enabled']
                tags_string = video_form.cleaned_data['tags']
                video = request.FILES['video']
                videopost = VideoPost()
                videopost.publication_date = datetime.datetime.now()
                videopost.title = title
                videopost.description = description
                videopost.enabled = enabled
                videopost.locked = True
                videopost.state = VideoPost.PENDING
                videopost.save()
                videopost_id = videopost.id
                save_tag(tags_string, videopost)
            except:
                variables['form'] = video_form
                messages.error(request, _('There was an error while saving the Video Post.'))
            try:
                path_absolute_temp = '%s%d' % (settings.PATH_TEMP, videopost_id)
                path_absolute_splash = '%s%d.jpeg' % (settings.PATH_SPLASH, videopost_id)
                create_splash = False
                destination = open(path_absolute_temp, 'wb+')
                for chunk in video.chunks():
                    destination.write(chunk)
                destination.close()
                if 'splash_image' in request.FILES:
                    splash_image = request.FILES['splash_image']
                    destination = open(path_absolute_splash, 'wb+')
                    for chunk in splash_image.chunks():
                        destination.write(chunk)
                    destination.close()
                else:
                    create_splash = True
                CreateVideopostTask.delay(videopost_id, create_splash)
                messages.success(request, _('Video Post successfully created. The video is currently being processed.'))
                return HttpResponseRedirect(reverse(admin_index))
            except:
                DeleteAsociatedFilesTask.delay(videopost_id)
                variables['form'] = video_form 
                messages.error(request, _('There was an error while uploading the file.'))
        else:
            messages.warning(request, _('Correct the errors bellow.'))                
    else:
        video_form = VideoPostCreateForm()
    variables['form'] = video_form 
    t = get_template('videopost/admin/create.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


@never_cache
@login_required        
def update(request, videopost_id):
    """
    Updates a Video Post
    """
    variables = dict()
    variables['title'] = _('Update Video Post')
    videopost = get_object_or_404(VideoPost, id=videopost_id)
    if request.POST:
        try:
            video_form = VideoPostUpdateForm(request.POST)
            if video_form.is_valid():
                title = video_form.cleaned_data['title']
                description = video_form.cleaned_data['description']
                enabled = video_form.cleaned_data['enabled']
                tags_string = video_form.cleaned_data['tags']
                videopost.publication_date = datetime.date.today()
                videopost.title = title
                videopost.description = description
                videopost.enabled = enabled
                videopost.save()
                videopost_id = videopost.id
                save_tag(tags_string, videopost)
                EditVideopostTask.delay(videopost_id)
                messages.success(request, _('Video Post successfully updated.'))
                return HttpResponseRedirect(reverse(admin_index))
            else:
                messages.warning(request, _('Correct the errors bellow.'))
        except:
            variables['form'] = video_form 
            messages.error(request, _('There was an error while updating the Video Post.'))
    else:
        try:
            videopost.tags.all()
            tags = ', '.join([video.name for video in videopost.tags.all()])            
            video_form = VideoPostUpdateForm(initial={'title': videopost.title,
                            'description': videopost.description,
                            'enabled': videopost.enabled,
                            'tags': tags, })            
            variables['title'] = videopost.title
            variables['videopost'] = videopost
        except:
            messages.error(request, _('There was an error while updating the Video Post.'))
    variables['form'] = video_form 
    t = get_template('videopost/admin/update.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


@never_cache
@login_required
def delete(request, videopost_id):
    """
    Deletes a Video Post
    """
    variables = dict()
    videopost_id = int(videopost_id)
    videopost = get_object_or_404(VideoPost, pk=videopost_id)
    if request.POST:
        try:
            videopost.delete()
            messages.success(request, _('Video Post successfully deleted.'))
            DeleteVideopostTask.delay(videopost_id)
        except:
            messages.error(request, _('There was an error while deleting the Video Post.'))
        return HttpResponseRedirect(reverse(admin_index))
    else:
            variables['videopost'] = videopost
            t = get_template('videopost/admin/delete.html')
            html = t.render(RequestContext(request, variables))
            return HttpResponse(html)   


@never_cache
@login_required
def admin_index(request, page="1"):
    """
    Loads the Administration panel for the Video Posts.
    """
    variables = dict()
    videopost_list = VideoPost.objects.all().order_by('-publication_date')
    max_results = 10
    if videopost_list:
        paginator_results, videoposts = paginator_numeric(videopost_list, max_results, page)
        variables.update(paginator_results)
        variables['videoposts'] = videoposts.object_list
        variables['pagination_list'] = videoposts
        variables['title'] = "Video Posts"
    else:
        messages.info(request, _('No Results Found.'))
    t = get_template('videopost/admin/list.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)

    
def save_tag(tags_string, videopost):
    """
    Saves the tags associated to a Video Post.
    """
    if tags_string.strip(): 
        tags = tags_string.lower().split(',')
        videopost.tags.clear()
        for tag_name in tags:
            tag_name = tag_name.strip()
            if len(tag_name):
                if Tag.objects.filter(name__iexact=tag_name).count():
                    tag = Tag.objects.get(name__iexact=tag_name)
                else:
                    tag = Tag()
                    tag.name = tag_name
                    tag.save()                 
                videopost.tags.add(tag)
        videopost.save()

