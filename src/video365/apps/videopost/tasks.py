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
from django.conf import settings
from video365.apps.videopost.models import VideoPost
from video365.helpers.generation_utils import generate_date_menu, \
    generate_tag_files, generate_tag_js
import os
import subprocess


class CreateVideopostTask(Task):
    """
    Converts the Video and creates the related files.
    """
    def run(self, videopost_id, create_splash, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Starting Video Post conversion: %s" % videopost_id)
        videopost = VideoPost.objects.get(pk=videopost_id)
        videopost.state = VideoPost.PROCESSING
        videopost.save()
        path_relative_videos = 'uploads/videos/%d.flv' % videopost_id
        path_relative_splash = 'uploads/splash/%d.jpeg' % videopost_id
        path_absolute_videos = '%s%d.flv' % (settings.PATH_VIDEOS, videopost_id)
        path_absolute_temp = '%s%d' % (settings.PATH_TEMP, videopost_id)
        path_absolute_splash = '%s%d.jpeg' % (settings.PATH_SPLASH, videopost_id)
        if create_splash:
            command_splash = ["ffmpeg", "-deinterlace", "-ss", "55", "-i", path_absolute_temp, "-y", "-vcodec", "mjpeg", "-vframes", "1", "-an", "-f", "rawvideo", path_absolute_splash]
            subprocess.call(command_splash, shell=False)
        command_convert = ["ffmpeg", "-i", path_absolute_temp, "-y", "-sameq", "-ar", "44100",  path_absolute_videos]
        p = subprocess.call(command_convert, shell=False)
        if p == 0:
            videopost.locked = False
            videopost.splash_image = path_relative_splash
            videopost.video = path_relative_videos
            videopost.state = VideoPost.READY
            videopost.save()
        else:
            videopost.state = VideoPost.ERROR
            videopost.save()
        try:
            os.remove(path_absolute_temp)
        except:
            pass
        generate_date_menu()
        generate_tag_files()
        generate_tag_js()
        return "Ready"


class DeleteAsociatedFilesTask(Task):
    """
    Deletes the Files related to a Video Post.
    """
    def run(self, videopost_id, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Starting Video Post files deletion %s" % videopost_id)
        path_absolute_videos = '%s%d.flv' % (settings.PATH_VIDEOS, videopost_id)
        path_absolute_temp = '%s%d' % (settings.PATH_TEMP, videopost_id)
        path_absolute_splash = '%s%d.jpeg' % (settings.PATH_SPLASH, videopost_id)
        try:
            os.remove(path_absolute_videos)
        except:
            pass
        try:
            os.remove(path_absolute_splash)
        except:
            pass
        try:
            os.remove(path_absolute_temp)
        except:
            pass
        return "Ready"


class DeleteVideopostTask(Task):
    """
    Deletes the Files related to a Video Post and generates new menus.
    """
    def run(self, videopost_id, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Starting Video Post deletion %s" % videopost_id)
        path_absolute_videos = '%s%d.flv' % (settings.PATH_VIDEOS, videopost_id)
        path_absolute_splash = '%s%d.jpeg' % (settings.PATH_SPLASH, videopost_id)
        try:
            os.remove(path_absolute_videos)
        except:
            pass
        try:
            os.remove(path_absolute_splash)
        except:
            pass
        generate_date_menu()
        generate_tag_files()
        generate_tag_js()
        return "Ready"


class EditVideopostTask(Task):
    """
    Generates new menus after the Update operation.
    """
    def run(self, videopost_id, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Starting Video Post edition %s" % videopost_id)
        generate_date_menu()
        generate_tag_files()
        generate_tag_js()
        return "Ready"
