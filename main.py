#!/usr/bin/env python
# -*- coding: utf-8 -*-

# muse-tray.py: main file
# 
# set up the basic status icon
#
# Author: YangZhang <zyangmath@gmail.com>
# Last updated:  2008-10-27 15:22:36
#

# Import the necessary modules
import gtk
from ui_statusicon import *
from app_globals import *

if __name__ == "__main__":
    
    global settings, wiki_list, app_info
    # Set up the enviroment of program
    settings.set_notes_dir("~/Documents/Muse/Notes/")
    settings.set_cache_dir("~/.cache/muse-icon/")
    settings.set_trash_dir("~/Documents/Muse/Notes/.trash/")

    wiki_list.set_wiki_dir(settings.get_notes_dir())
    wiki_list.update_wiki_list()

    app_info.init()
    
    app_main_ui = AppStatusIconUI()
    app_main_ui.run()

