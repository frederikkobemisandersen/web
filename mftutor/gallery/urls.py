# encoding: utf8
from __future__ import unicode_literals
from django.conf.urls import url
import mftutor.gallery.views
from mftutor.tutor.auth import tutorbest_required, tutor_required

urlpatterns = [
    # Gallery overview
    url(r'^$',
        tutor_required(mftutor.gallery.views.gallery),
        name='gallery_index'),
    url(r'^(?P<gfyear>\d+)$',
        mftutor.gallery.views.gallery,
        name='gfyear'),

    # Album overview
    url(r'^(?P<gfyear>\d+)/(?P<album_slug>[^/]+)$',
        tutor_required(mftutor.gallery.views.album),
        name='album'),

    # Single images
    url(r'^(?P<gfyear>\d+)/(?P<album_slug>[^/]+)/(?P<image_slug>[^/]+)$',
        tutor_required(mftutor.gallery.views.image),
        name='image'),

    # Bulk-update BaseMedia.visibility
    url(r'^set_visibility/$',
        tutorbest_required(mftutor.gallery.views.set_visibility),
        name='set_image_visibility'),

    # JFU upload
    url(r'^upload/',
        tutorbest_required(mftutor.gallery.views.upload),
        name='jfu_upload'),
]
