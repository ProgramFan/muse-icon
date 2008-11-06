#!/usr/bin/env python
#-*- coding: utf-8 -*-

## the settings of the program

import os
import gtk

class Settings():
    "Setting of the program"
    def __init__(self):
        self.muse_notes_dir = None
        self.html_cache_dir = None
        self.muse_trash_dir = None
        self.max_main_menu_item = 10
    
    def set_notes_dir(self, directory):
        self.muse_notes_dir = os.path.abspath(os.path.expanduser(directory))

    def set_cache_dir(self, directory):
        self.html_cache_dir = os.path.abspath(os.path.expanduser(directory))
        if not os.path.exists(self.html_cache_dir):
            os.system("mkdir " + self.html_cache_dir)

    def set_trash_dir(self, directory):
        self.muse_trash_dir = os.path.abspath(os.path.expanduser(directory))
        if not os.path.exists(self.muse_trash_dir):
            os.system("mkdir " + self.muse_trash_dir)

    def set_max_main_menu_item(self, number):
        self.max_main_menu_item = number
    
    def get_notes_dir(self):
        return self.muse_notes_dir

    def get_cache_dir(self):
        return self.html_cache_dir

    def get_trash_dir(self):
        return self.muse_trash_dir

class AppInfo():
    def __init__(self):
        self.name = "Muse Icon"
        self.version = "0.05"
        self.authors = ["YangZhang <zyangmath@gmail.cim>, 2008"]
        self.license = "GNU GPL"
        self.copyright = "Copyright (C) 2008, YangZhang"
        self.comments = "View and edit your Emacs/Muse wikis via system tray"
        self.translator_credits = "translator credit"
        app_icon_factory = gtk.Invisible()
        self.app_icon = app_icon_factory.render_icon(gtk.STOCK_EDIT, gtk.ICON_SIZE_DIALOG)
  
    def init(self):
        self.__init__()

class WikiList():
    " Manage a list of avaliable wikis under a directory"
    def __init__(self, directory = None, file_extension = ".muse"):
        if directory:
            self.wiki_directory = os.path.abspath(os.path.expanduser(directory))
        else:
            self.wiki_directory = None
        self.wiki_extension = file_extension
        self.wiki_list = []
        self.__build_list()

    def __build_list(self):
        self.wiki_list = [ os.path.join(self.wiki_directory, fname) 
                           for fname in os.listdir(self.wiki_directory) 
                           if  os.path.splitext(fname)[-1] == self.wiki_extension 
                           and os.path.isfile(os.path.join(self.wiki_directory, fname)) ]
        self.wiki_list.sort(key = lambda x: os.lstat(x).st_mtime, reverse=True)

    def set_wiki_dir(self, directory):
        if directory:
            self.wiki_directory = os.path.abspath(os.path.expanduser(directory))
            
    def get_wiki_list(self):
        return self.wiki_list

    def update_wiki_list(self):
        self.__build_list()

if __name__ == "__main__":
    pass
