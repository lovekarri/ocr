#!/bin/bash

main_path='/paddle/ocr/main.py'

pid=$(ps -ef | grep "python $main_path" | grep -v grep | awk '{print $2}')

if [ -n "$pid" ]; then
    kill $pid
fi