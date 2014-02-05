#!/bin/bash

RUN_CMD="`which django-admin.py` test oath_toolkit.django_otp"
[[ "$1" == "COVERAGE" ]] && RUN_CMD="coverage run $RUN_CMD"

cd `dirname $0`/..
PYTHONPATH=tests DJANGO_SETTINGS_MODULE=test_django.settings $RUN_CMD
EXIT=$?
[[ "$1" == "COVERAGE" ]] && coverage report -m
exit $EXIT
