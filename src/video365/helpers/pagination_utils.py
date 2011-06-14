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
from django.core.paginator import Paginator


def paginator_simple(items_list, max_results, page):
    paginator = Paginator(items_list, max_results)
    try:
        page = int(page)
    except:
        page = 1    
    try:
        result_paginated = paginator.page(page)
    except:
        result_paginated = paginator.page(paginator.num_pages)
    return result_paginated


def paginator_numeric(items, max_results, page):
    variables = dict()
    paginator = Paginator(items, max_results)
    page = int(page)
    page_range = list()
    try:
        items = paginator.page(int(page))
    except:
        items = paginator.page(paginator.num_pages)
    if paginator.num_pages > 15:
        last_page = paginator.num_pages
        if page <= 6:
            places = (7 -  page) + 1            
            page_range.extend(range(1, page+places))
            page_range.append('...')
            page_range.extend(range(paginator.num_pages-2, last_page+1))
        elif page >= last_page - 4:
            places = 6 - (last_page - page)
            page_range.extend(range(1, 4))
            page_range.append('...')
            page_range.extend(range(page - places, last_page+1))
        else:
            page_range.extend(range(1, 4))            
            page_range.append('...')
            page_range.extend(range(page - 1, page + 2))
            page_range.append('...')
            page_range.extend(range(paginator.num_pages-2, last_page+1))
    else:
        page_range.extend(range(1, paginator.num_pages+1))
    variables['total_pages'] = paginator.num_pages
    variables['page_range'] = page_range
    return variables, items
