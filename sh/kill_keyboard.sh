#!/bin/bash

ps -ef | grep matchbox-keyboard | awk '{print $2}' | xargs kill

