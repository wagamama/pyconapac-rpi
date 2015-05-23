#!/bin/bash

ps -ef | grep python | grep regist | awk '{print $2}' | xargs kill

