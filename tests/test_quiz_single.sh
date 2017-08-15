#!/bin/sh

echo -n "Test quiz single ... "
curl -X POST -d@- localhost:9206/quiz/test-single <<EOF
{
    "q1": "blue",
    "q2": true
}
EOF

echo
echo -n "Test quiz single ... "
curl -X POST -d@- localhost:9206/quiz/test-single <<EOF
{
    "q1": "blue",
    "q2": false 
}
EOF

echo
echo -n "Test quiz single ... "
curl -X POST -d@- localhost:9206/quiz/test-single <<EOF
{
    "q1": "green",
    "q2": false 
}
EOF
