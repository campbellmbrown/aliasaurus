#!/bin/bash

git rev-parse --short=8 HEAD > resources/GIT_SHA
pyinstaller --onefile --noconsole --add-data "resources;resources" aliasaurus.py
