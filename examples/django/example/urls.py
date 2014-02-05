from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urls = (
    # Examples:
    url(r'^$', 'example.views.index', name='index'),
    url(r'^protected/$', 'example.views.protected', name='protected'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/tfa/$', 'example.views.otp_status', name='otp_status'),
    url(r'^accounts/tfa/setup/$', 'example.views.otp_setup', name='otp_setup'),
    url(r'^accounts/tfa/setup/qrcode/$', 'example.views.otp_qrcode',
        name='otp_qrcode'),
    url(r'^accounts/tfa/setup/verify/$', 'example.views.otp_setup_verify',
        name='otp_setup_verify'),
    url(r'^accounts/verify/$', 'example.views.otp_verify', name='otp_verify'),
    url(r'^accounts/', include('django.contrib.auth.urls', 'auth'))
)

urlpatterns = patterns('', *urls)
