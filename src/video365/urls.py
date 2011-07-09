# -*- coding: utf-8 -*-
'''
Copyright Cobalys (c) 2011

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
from django.conf.urls.defaults import *
from video365.apps.administration import views as administration_views
from video365.apps.tag import views as tag_views
from video365.apps.videopost import views as videopost_views
import video365.settings

urlpatterns = patterns('',
    (r'^permalink/(?P<videopost_id>\d+)/$', videopost_views.retrieve),  # Retrieve
    (r'^(?P<videopost_id>\d+)/([\w-]+).html$', videopost_views.retrieve),  #Retrieve
    (r'^(?P<page>\d+)/$', videopost_views.retrieve_all),  #Retrieve All
    (r'^date/(?P<page>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', videopost_views.get_by_date),  #Search by Date
    (r'^date/(?P<page>\d+)/(?P<year>\d{4})/(?P<month>\d+)/$', videopost_views.get_by_date),  #Search by Date
    (r'^date/(?P<page>\d+)/(?P<year>\d{4})/$', videopost_views.get_by_date),  #Search by Date
    (r'^tag/(?P<tag_id>\d+)/(?P<page>\d+)/([\w-]+).html$', videopost_views.get_by_tag),  #Search by Tag
    (r'^tag/(?P<tag_id>\d+)/([\w-]+).html$', videopost_views.get_by_tag),  #Search by Tag 
)

urlpatterns += patterns('',  
    (r'^admin/videopost/(?P<page>\d+)$', videopost_views.admin_index), #Videopost Administration Panel.
    (r'^admin/videopost/$', videopost_views.admin_index),  #Videopost Administration Panel.
    (r'^admin/videopost/create/$', videopost_views.create),  #Create
    (r'^admin/videopost/update/(?P<videopost_id>\d+)/$', videopost_views.update),  #Update
    (r'^admin/videopost/delete/(?P<videopost_id>\d+)/$', videopost_views.delete),  #Delete
)

urlpatterns += patterns('',  
    (r'^admin/tag/$', tag_views.admin_index),  #Tags Administration Panel.
    (r'^admin/tag/create/$', tag_views.create),  #Create
    (r'^admin/tag/edit/(?P<tag_id>\d+)/$', tag_views.update),  #Update
    (r'^admin/tag/delete/(?P<tag_id>\d+)/$', tag_views.delete),  #Delete
)

urlpatterns += patterns('',
    (r'^admin/$', administration_views.admin_panel),                          
    (r'^admin/change-password/$', administration_views.change_password),
    (r'^admin/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    (r'^admin/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'admin/logout.html'}),
)

urlpatterns += patterns('',        
    (r'^index.html$', videopost_views.retrieve_all),
    (r'^$', videopost_views.retrieve_all),   
)