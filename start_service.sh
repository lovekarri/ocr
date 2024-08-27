#!/bin/bash

main_path='/paddle/ocr/main.py'

# 检查是否已经有这个脚本在运行
pid=$(ps -ef | grep "$main_path" | grep -v grep | awk '{print $2}')

if [ -z "$pid" ]; then
    python $main_path
else
    echo "服务已经在运行，不重复开启。"
fi
