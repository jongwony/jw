#!/usr/bin/env bash

cat $3 | mysql --defaults-group-suffix=_$1 --init-command="set names 'utf8mb4'" --show-warnings -vvv $2 2>&1 | vim -u ~/.vimrc.more -
