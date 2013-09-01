#!/bin/sh
# Running this testsuite assumes that you've modified the oathtool test script
# to run arbitrary OATHTOOL executables.
# Also, it assumes that you have set OATH_TOOLKIT_DIR to the top-level
# directory of the oath-toolkit sources.

OATHTOOL=`dirname $0`/pyoathtool \
    $OATH_TOOLKIT_DIR/oathtool/tests/tst_oathtool.sh
