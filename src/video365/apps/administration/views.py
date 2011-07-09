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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache


@never_cache
@login_required
def admin_panel(request):
    t = get_template('admin/index.html')
    html = t.render(RequestContext(request))
    return HttpResponse(html)

@never_cache
@login_required
def change_password(request):
    variables = dict()
    if request.POST:
        try:
            configuration_form = PasswordChangeForm(user=request.user, data=request.POST)
            if configuration_form.is_valid():
                configuration_form.save()
                messages.success(request, _('Password changed.'))
                return HttpResponseRedirect(reverse(admin_panel))
            else:
                messages.warning(request, _('Correct the errors bellow.'))
        except:
            messages.error(request, _('There was an error while changing the Password.'))
    else:
        configuration_form = PasswordChangeForm(user=request.user)
    variables['form'] = configuration_form
    t = get_template('admin/change-password.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)
