#!/bin/sh

ssh_tunnel() {
    ps ux | grep ssh | grep dredd | awk '{print $2}' | xargs kill
    ssh -f -N -R 9206:localhost:9206 -o ServerAliveInterval=60 dredd.yld.me
}

ssh_tunnel
python dredd --logging=debug --debug
