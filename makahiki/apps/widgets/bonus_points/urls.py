"""urls definition for bonus_points widget."""
'''
Created on Aug 5, 2012

@author: Cam Moore
'''

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^bonus_code/$',
        'apps.widgets.bonus_points.views.bonus_code',
        name="bonus_points_code"),
    url(r'^view_codes/$',
        'apps.widgets.bonus_points.view_bonus_points.view_codes',
        name='bonus_view_codes'),
)
