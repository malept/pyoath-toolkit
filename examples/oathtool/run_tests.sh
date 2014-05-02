#!/bin/bash
#
# Downloads and runs the oathtool testsuite from a given git revision of
# oath-toolkit.

[[ -z "$DOWNLOAD_DIR" ]] && DOWNLOAD_DIR=/tmp

SHA1=38a385079b36d7f95d685055a13177a62ffe7d79
GIT_TAG=oath-toolkit-2-4-1

TEST=tst_oathtool.sh
TEST_PATH="$DOWNLOAD_DIR/$TEST"

if [[ ! -f "$TEST_PATH" ]]; then
    wget -O "$TEST_PATH" "https://raw.githubusercontent.com/malept/oath-toolkit/$GIT_TAG/oathtool/tests/$TEST"

    echo "$SHA1  $TEST_PATH" > "$TEST_PATH".sha1sum

    if ! sha1sum --check --strict "$TEST_PATH".sha1sum; then
        echo 'SHA1 checksum does not match.' >&2
        exit 1
    fi

    sed -i -e '/OATHTOOL=/d' "$TEST_PATH"
    chmod +x "$TEST_PATH"
fi

OATHTOOL=`dirname $0`/pyoathtool "$TEST_PATH"
