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
from celery.task import Task
from video365.helpers.generation_utils import generate_date_menu, \
    generate_tag_files, generate_tag_js


class UpdateTagFilesTask(Task):
    """
    Updates the generated files.
    """
    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Starting Tag Deletion...")
        generate_date_menu()
        generate_tag_files()
        generate_tag_js()
        return "Ready"
