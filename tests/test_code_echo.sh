#!/bin/sh

# Bash

SOURCE=$(mktemp -t dredd_XXXXXXX.sh)
cat > $SOURCE <<EOF
cat
EOF
echo -n "Testing Bash ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Python

SOURCE=$(mktemp -t dredd_XXXXXXX.py)
cat > $SOURCE <<EOF
import sys
for line in sys.stdin:
    print(line.rstrip())
EOF
echo
echo -n "Testing Python ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# C

SOURCE=$(mktemp -t dredd_XXXXXXX.c)
cat > $SOURCE <<EOF
#include <stdio.h>
#include <stdlib.h>
void main() {
    char buffer[BUFSIZ];
    while (fgets(buffer, BUFSIZ, stdin))
	fputs(buffer, stdout);
}
EOF
echo
echo -n "Testing C ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# C++

SOURCE=$(mktemp -t dredd_XXXXXXX.cpp)
cat > $SOURCE <<EOF
#include <iostream>
#include <string>
using namespace std;
int main() {
    string line;
    while (getline(cin, line))
	cout << line << endl;
    return 0;
}
EOF
echo
echo -n "Testing C++ ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Ruby

SOURCE=$(mktemp -t dredd_XXXXXXX.rb)
cat > $SOURCE <<EOF
ARGF.each do |line|
    puts line
end
EOF
echo
echo -n "Testing Ruby ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Java

SOURCE=$(mktemp -t dredd_XXXXXXX.java)
cat > $SOURCE <<EOF
import java.util.Scanner;

public class $(basename $SOURCE .java) {
    public static void main(String[] args) {
	Scanner scanner = new Scanner(System.in);
	while (scanner.hasNextLine()) {
	    System.out.println(scanner.nextLine());
	}
	scanner.close();
    }
}
EOF
echo
echo -n "Testing Java ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# JavaScript

SOURCE=$(mktemp -t dredd_XXXXXXX.js)
cat > $SOURCE <<EOF
var readline = require('readline');
var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});
rl.on('line', function (line) {
    console.log(line);
});
EOF
echo
echo -n "Testing JavaScript ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Go

SOURCE=$(mktemp -t dredd_XXXXXXX.go)
cat > $SOURCE <<EOF
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
	    fmt.Println(scanner.Text())
	}
}
EOF
echo
echo -n "Testing Go ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Guile

SOURCE=$(mktemp -t dredd_XXXXXXX.scm)
cat > $SOURCE <<EOF
(use-modules (ice-9 rdelim))
(define file (current-input-port))
(do ((line (read-line file) (read-line file))) ((eof-object? line))
    (display line)
    (newline))
EOF
echo
echo -n "Testing Guile ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Perl6

SOURCE=$(mktemp -t dredd_XXXXXXX.pl)
cat > $SOURCE <<EOF
for lines() {
    say \$_;
}
EOF
echo
echo -n "Testing Perl6 ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Rust

SOURCE=$(mktemp -t dredd_XXXXXXX.rs)
cat > $SOURCE <<EOF
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        println!("{}", line.unwrap());
    }
}
EOF
echo
echo -n "Testing Rust ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Haskell

SOURCE=$(mktemp -t dredd_XXXXXXX.hs)
cat > $SOURCE <<EOF
main = interact id
EOF
echo
echo -n "Testing Haskell ... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# Swift 5.3
SOURCE=$(mktemp -t dredd_XXXXXXX.swift)
cat > $SOURCE <<EOF
while let line = readLine() {
    print(line)
}
EOF
echo
echo -n "Testing Swift 5.3 ..."
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# # Brainfuck
# 
# SOURCE=$(mktemp -t dredd_XXXXXXX.bf)
# cat > $SOURCE <<EOF
# ,+[-.,+]
# EOF
# echo
# echo -n "Testing Brainfuck ... "
# curl -F source=@$SOURCE localhost:9206/code/test-echo
# rm -f $SOURCE

# # Perl
# 
# SOURCE=$(mktemp -t dredd_XXXXXXX.pl)
# cat > $SOURCE <<EOF
# use strict;
# use warnings;
# 
# while (my $line = <>) {
#     print($line);
# }
# EOF
# echo
# echo -n "Testing Perl ... "
# curl -F source=@$SOURCE localhost:9206/code/test-echo
# rm -f $SOURCE

# C (Compiler Error)

SOURCE=$(mktemp -t dredd_XXXXXXX.c)
cat > $SOURCE <<EOF
#include <stdio.h>
#include <stdlib.h>
void main() {
    char buffer[BUFSIZ];
    while (fgets(buffer, BUFSIZ, stdin))
	fputs(buffer, stdout)
}
EOF
echo
echo -n "Testing C (Compiler Error)... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# C (Execution Error)

SOURCE=$(mktemp -t dredd_XXXXXXX.c)
cat > $SOURCE <<EOF
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]) {
    puts(argv[1000]);
    return 0;
}
EOF
echo
echo -n "Testing C (Execution Error)... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# C (Wrong Answer)

SOURCE=$(mktemp -t dredd_XXXXXXX.c)
cat > $SOURCE <<EOF
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]) {
    char buffer[BUFSIZ];
    while (fgets(buffer, BUFSIZ, stdin))
	fprintf(stdout, "1%s", buffer);
    return 0;
}
EOF
echo
echo -n "Testing C (Wrong Answer)... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# C (Time Limit)

SOURCE=$(mktemp -t dredd_XXXXXXX.c)
cat > $SOURCE <<EOF
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(int argc, char *argv[]) {
    sleep(100);
    return 0;
}
EOF
echo
echo -n "Testing C (Time Limit)... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE

# C (Wrong Formatting)

SOURCE=$(mktemp -t dredd_XXXXXXX.c)
cat > $SOURCE <<EOF
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]) {
    char buffer[BUFSIZ];
    while (fgets(buffer, BUFSIZ, stdin))
	fprintf(stdout, " %s", buffer);
    return 0;
}
EOF
echo
echo -n "Testing C (Wrong Formatting)... "
curl -F source=@$SOURCE localhost:9206/code/test-echo
rm -f $SOURCE
