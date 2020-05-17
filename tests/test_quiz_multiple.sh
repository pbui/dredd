#!/bin/sh

echo -n "Test quiz multiple ... "
curl -d@- localhost:9206/quiz/test-multiple <<EOF
{
    "q1": [
	"blue",
	"green"
    ],
    "q2": [
	"pizza",
	"tacos"
    ]
}
EOF

echo
echo -n "Test quiz multiple ... "
curl -d@- localhost:9206/quiz/test-multiple <<EOF
{
    "q1": [
	"blue",
	"red"
    ],
    "q2": [
	"pizza",
	"hamburger"
    ]
}
EOF

echo
echo -n "Test quiz multiple ... "
curl -d@- localhost:9206/quiz/test-multiple <<EOF
{
    "q1": [
	"green",
	"red"
    ],
    "q2": [
	"hamburger",
	"pizza"
    ]
}
EOF

echo
echo -n "Test quiz multiple ... "
curl -d@- localhost:9206/quiz/test-multiple <<EOF
{
    "q1": [
	"blue"
    ],
    "q2": [
	"",
	"tacos"
    ]
}
EOF
