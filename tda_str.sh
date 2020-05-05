#!/bin/bash
ps x | grep 'tda_streaming' | awk '{print $1}' | xargs kill -9
# please change the path to the proper place (both the python binary and the script)
/path/to/your/python /path/to/your/tda_streaming.py
