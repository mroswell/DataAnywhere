#!/bin/bash
for i in `ps awux | grep uwsgi | grep -v grep | awk '{print $2}'`
do
    echo "killing $i..."
    sudo kill -9 $i
done
