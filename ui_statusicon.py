#!/usr/bin/env python
#-*- coding: utf-8 -*-

import gtk
import os
from muse_helper import *
from ui_viewer import *
from app_globals import *

class AppStatusIconUI():

    def __main_quit(self, widget):
        gtk.main_quit()

    def __check_emacs(self):
        emacs_socket_dir = "/tmp/emacs" + str(os.getuid())
        if not os.path.exists(emacs_socket_dir):
            return False
        if os.listdir(emacs_socket_dir):
            return True
        else:
            return False

    def __edit_file(self, widget, fname = None):
        global settings, app_info
        if self.__check_emacs():
            muse_notes_dir = settings.get_notes_dir()
            emacs_cmd = "emacsclient --no-wait " + os.path.join(muse_notes_dir, "index.muse")
            os.system(emacs_cmd)
        else:
            alert_dialog = gtk.MessageDialog(parent = None,
                                             type = gtk.MESSAGE_WARNING,
                                             buttons = gtk.BUTTONS_OK)
            alert_dialog.set_icon(app_info.app_icon)
            alert_dialog.set_title(u"信息")
            alert_dialog.set_markup(u"<b>Emacs server 尚未启动</b>\n请以 server 模式启动 emacs。")
            alert_dialog.run()
            alert_dialog.destroy()

    def __view_file(self, widget, fname):
        viewer = MuseWikiViewer(fname)
        viewer.show()

    def __show_pref_dialog(self, widget):
        global app_info
        dialog = gtk.Dialog()
        dialog.set_title("Preference")
        dialog.set_icon(app_info.app_icon)
        dialog.set_geometry_hints(min_width = 300, min_height = 400)
        dialog.run()
        dialog.destroy()

    def __show_about_dialog(self, widget):
        global app_info
        app_icon = app_info.app_icon
        dialog = gtk.AboutDialog()
        dialog.set_icon(app_icon)
        dialog.set_logo(app_icon)
        dialog.set_name(app_info.name)
        dialog.set_version(app_info.version)
        dialog.set_copyright(app_info.copyright)
        dialog.set_comments(app_info.comments)
        dialog.set_license(app_info.license)
        dialog.set_authors(app_info.authors)
        dialog.set_translator_credits(app_info.translator_credits)
        dialog.run()
        dialog.destroy()

    def __show_popup_menu(self, widget, button, time):
        # Only activate when right clicked
        if button == 3:
            menu = gtk.Menu()
            menu_item = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
            menu_item.connect("activate", self.__show_pref_dialog)
            menu.append(menu_item)
            menu_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
            menu_item.connect("activate", self.__show_about_dialog)
            menu.append(menu_item)
            menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
            menu_item.connect("activate", self.__main_quit)
            menu.append(menu_item)
            menu.show_all()
            menu.popup(None, None, gtk.status_icon_position_menu,
                       button, time, widget)

    def __show_main_menu(self, widget):
        global settings
        menu = gtk.Menu()
        menu_item = gtk.ImageMenuItem(gtk.STOCK_ADD)
        menu_item.connect("activate", self.__edit_file, os.path.join(settings.get_notes_dir(), "index.muse"))
        menu.append(menu_item)
        menu_item = gtk.SeparatorMenuItem()
        menu.append(menu_item)
        wiki_list.update_wiki_list()
        file_list = wiki_list.get_wiki_list()
        length = len(file_list)
        max_menu_item = settings.max_main_menu_item
        if length > max_menu_item:
            length = 10
        for fname in file_list[0:length]:
            wiki = MuseWiki(fname)
            item_label = wiki.get_title()
            menu_item = gtk.MenuItem(item_label)
            menu_item.connect("activate", self.__view_file, fname)
            menu.append(menu_item)
        if len(file_list) > max_menu_item:
            sub_menu = gtk.Menu()
            for fname in file_list[max_menu_item:len(file_list)]:
                wiki = MuseWiki(fname)
                item_label = wiki.get_title()
                menu_item = gtk.MenuItem(item_label)
                menu_item.connect("activate", self.__view_file, fname)
                sub_menu.append(menu_item)
            menu_item = gtk.MenuItem(u"更多笔记")
            menu_item.set_submenu(sub_menu)
            menu.append(menu_item)
        menu_item = gtk.SeparatorMenuItem()
        menu.append(menu_item)
        menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menu_item.connect("activate", self.__main_quit)
        menu.append(menu_item)
        menu.show_all()
        event = gtk.get_current_event()
        if event:
            menu.popup(None, None, gtk.status_icon_position_menu, 
                       event.button, event.time, widget)

    def __init__(self):
        global app_info
        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_stock(gtk.STOCK_EDIT)
        self.statusicon.connect("activate", self.__show_main_menu)
        self.statusicon.connect("popup-menu", self.__show_popup_menu)

    def run(self):
        self.statusicon.set_visible(True)
        gtk.main()


