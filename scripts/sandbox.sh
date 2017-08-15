#!/bin/sh

IMAGE=dredd:20170814

if [ $# -ne 5 ]; then
    echo "Usage: $(basename $0) sandbox runner source"
    exit 1
fi

SANDBOX_PATH=$(readlink -f ${1})
RUNNER_PATH=${2}
SOURCE_PATH=${3}
INPUT_PATH=${4}
OUTPUT_PATH=${5}

if [ ! -d "$SANDBOX_PATH" ]; then
    mkdir -p "$SANDBOX_PATH"
fi

cp -f "$RUNNER_PATH" "$SANDBOX_PATH"
cp -f "$SOURCE_PATH" "$SANDBOX_PATH"
cp -f "$INPUT_PATH" "$SANDBOX_PATH"
cp -f "$OUTPUT_PATH" "$SANDBOX_PATH"

docker run -i -w /sandbox -v "$SANDBOX_PATH":/sandbox $IMAGE ./$(basename $RUNNER_PATH) $(basename $SOURCE_PATH) $(basename $INPUT_PATH) $(basename $OUTPUT_PATH)

# vim: set sts=4 sw=4 ts=8 expandtab ft=sh:
