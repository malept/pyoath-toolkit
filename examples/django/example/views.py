# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as u_, ugettext_lazy as ul_
from django_otp import devices_for_user, login as otp_login
from django_otp.decorators import otp_required
from django_otp.forms import OTPTokenForm
from oath_toolkit.django_otp.totp.models import (
    OToolkitTOTPDevice as TOTPDevice)
from .forms import DeviceValidationForm


def index(request):
    return render(request, 'index.html')


@otp_required
def protected(request):
    return render(request, 'protected.html')


@login_required
def otp_status(request):
    tfa_enabled = len(list(devices_for_user(request.user, True))) > 0
    if tfa_enabled:
        tfa_status = ul_(u'enabled')
        tfa_btn_name = 'disable'
        tfa_btn_value = ul_(u'Disable')
    else:
        tfa_status = ul_(u'disabled')
        tfa_btn_name = 'enable'
        tfa_btn_value = ul_(u'Enable')
    return render(request, 'otp_status.html', {
        'tfa_status': tfa_status,
        'tfa_button_name': tfa_btn_name,
        'tfa_button_value': tfa_btn_value,
    })


@login_required
def otp_setup(request):
    confirmed_devices = list(devices_for_user(request.user, True))
    tfa_enabled = len(confirmed_devices) > 0
    if request.method == 'GET' and not tfa_enabled:
        unconfirmed_devices = list(devices_for_user(request.user, False))
        device = unconfirmed_devices[0]
        form = DeviceValidationForm(device)
        return render(request, 'otp_setup.html', {
            'device': device,
            'form': form,
        })
    elif request.method == 'POST':
        if request.POST.get(u'enable') and not tfa_enabled:
            device = TOTPDevice.objects.create(user=request.user,
                                               name=u'TOTP',
                                               confirmed=False)
            form = DeviceValidationForm(device)
            return render(request, 'otp_setup.html', {
                'device': device,
                'form': form,
            })
        elif request.POST.get(u'disable') and tfa_enabled:
            for device in confirmed_devices:
                device.delete()
            messages.success(request, u_(
                u'Disabled two-factor authentication for this account.'))
        else:
            messages.error(request, u_(u'Unknown error.'))
    return redirect('otp_status')


@login_required
def otp_setup_verify(request):
    if request.method == 'POST':
        unconfirmed_devices = list(devices_for_user(request.user, False))
        device = unconfirmed_devices[0]
        form = DeviceValidationForm(device, request.POST)
        if form.is_valid():
            device.confirmed = True
            device.save()
            messages.success(request, u_(
                u'Enabled two-factor authentication for this account.'))
        else:
            return redirect('otp_setup')
    else:
        messages.error(request, u_(u'Unknown error.'))
    return redirect('otp_status')


@login_required
def otp_qrcode(request):
    response = None
    for device in devices_for_user(request.user, False):
        if not hasattr(device, 'secret_qrcode'):
            continue
        qrcode = device.secret_qrcode(request)
        response = HttpResponse(content_type='image/png')
        qrcode.save(response, 'PNG')
    if not response:
        raise Http404
    return response


@login_required
def otp_verify(request):
    if request.method == 'POST':
        redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                       request.GET.get(REDIRECT_FIELD_NAME,
                                                       ''))
        form = OTPTokenForm(request.user, request, request.POST)
        if form.is_valid():
            otp_login(request, request.user.otp_device)
            # Ensure the user-originating redirection url is safe.
            # From django.contrib.auth.views.login
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            return HttpResponseRedirect(redirect_to)
    else:
        form = OTPTokenForm(request.user, request)
    return render(request, 'otp_verify.html', {
        'form': form,
    })
