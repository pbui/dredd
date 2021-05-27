#!/bin/sh

if [ $# -ne 5 ]; then
    echo "Usage: $(basename $0) sandbox runner source"
    exit 1
fi

SANDBOX_PATH=$(readlink -f ${1})
RUNNER_PATH=${2}
SOURCE_PATH=${3}
INPUT_PATH=${4}
OUTPUT_PATH=${5}

#IMAGE=pbui/dredd-code:20191004
IMAGE=pbui/dredd-code:20200506
IMAGE=pbui/dredd-code:20200715
IMAGE=pbui/dredd-code:20210524

if [ ! -d "$SANDBOX_PATH" ]; then
    mkdir -p "$SANDBOX_PATH"
fi

if [ -r $(dirname $INPUT_PATH)/timeout ]; then
    TIMEOUT="-t $(cat $(dirname $INPUT_PATH)/timeout)"
fi

cp -f "$RUNNER_PATH" "$SANDBOX_PATH"
cp -f "$SOURCE_PATH" "$SANDBOX_PATH" > /dev/null 2>&1
cp -f "$INPUT_PATH" "$SANDBOX_PATH"  > /dev/null 2>&1
cp -f "$OUTPUT_PATH" "$SANDBOX_PATH" > /dev/null 2>&1

docker run -e DEBUG=${DEBUG:-0} -i -w /sandbox -v "$SANDBOX_PATH":/sandbox $IMAGE \
    ./$(basename $RUNNER_PATH) $TIMEOUT \
        $(basename $SOURCE_PATH) \
        $(basename $INPUT_PATH) \
        $(basename $OUTPUT_PATH)

# vim: set sts=4 sw=4 ts=8 expandtab ft=sh:
