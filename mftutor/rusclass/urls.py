from django.conf.urls import patterns, url

from mftutor.tutor.auth import tutorbur_required
from mftutor.rusclass.views import TutorListView

urlpatterns = patterns('',
    url(r'^$', tutorbur_required(TutorListView.as_view()),
        name='tutor_list_pdf'),
)
