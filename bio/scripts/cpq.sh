#!/usr/bin/env bash

echo "$(pbpaste)\\Gshow profile\\G" | mysql --defaults-group-suffix=_$1 --init-command="set profiling=1" $2 | vim -u ~/.vimrc.more -
