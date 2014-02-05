#!/bin/bash

RUN_CMD="`which django-admin.py` test oath_toolkit.django_otp"
[[ "$1" == "COVERAGE" ]] && RUN_CMD="coverage run $RUN_CMD"

BASE_DIR=`dirname $0`/..
cd "$BASE_DIR"
PPATH="$BASE_DIR/tests"
[[ -n "$PYOTK_UNINSTALLED" ]] && PPATH="$PPATH:$BASE_DIR"
PYTHONPATH="$PPATH" DJANGO_SETTINGS_MODULE=test_django.settings $RUN_CMD
EXIT=$?
[[ "$1" == "COVERAGE" ]] && coverage report -m
exit $EXIT
