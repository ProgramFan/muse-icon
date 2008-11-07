#!/usr/bin/env python
#-*- coding: utf-8 -*-

## the wiki viewer

import gtk
import gtkhtml2
from urlparse import urlparse
from muse_helper import *
from app_globals import *

class History():
    " An implementation of browse history"
    def __init__(self):
        self.__history = []
        self.current = -1

    def push(self, item):
        self.__history = self.__history[0:self.current+1]
        self.__history.append(item)
        self.current += 1

    def can_go_forward(self):
        return self.current < len(self.__history) -1

    def go_forward(self):
        if not self.can_go_forward():
            return None
        self.current += 1
        return self.__history[self.current]

    def can_go_back(self):
        return self.current > 0

    def go_back(self):
        if not self.can_go_back():
            return None
        self.current -= 1
        return self.__history[self.current]

    def get_current(self):
        if self.current == -1:
            return None
        else:
            return self.__history[self.current]

    def clear(self):
        self.__init__()
    
class MuseWikiViewer():
    " A GTK+ Muse Wiki Viewer "
    def __check_emacs(self):
        emacs_socket_dir = "/tmp/emacs" + str(os.getuid())
        if not os.path.exists(emacs_socket_dir):
            return False
        if os.listdir(emacs_socket_dir):
            return True
        else:
            return False

    def __new_note(self, widget):
        global settings, app_info
        muse_notes_dir = settings.get_notes_dir()
        if self.__check_emacs():
            emacs_cmd = "emacsclient --no-wait " + os.path.join(muse_notes_dir, "index.muse")
            os.system(emacs_cmd)
        else:
            alert_dialog = gtk.MessageDialog(parent = self.window,
                                             type = gtk.MESSAGE_INFO,
                                             buttons = gtk.BUTTONS_OK)
            alert_dialog.set_title(u"信息")
            alert_dialog.set_icon(app_info.app_icon)
            alert_dialog.set_markup(u"<b>Emacs server 尚未启动</b>\n请以 server 模式启动 emacs。")
            alert_dialog.run()
            alert_dialog.destroy()

    def __edit_note(self, widget):
        global app_info
        if self.__check_emacs():
            emacs_cmd = "emacsclient --no-wait " + self.wiki.wiki_file
            os.system(emacs_cmd)
        else:
            alert_dialog = gtk.MessageDialog(parent = self.window,
                                             type = gtk.MESSAGE_INFO,
                                             buttons = gtk.BUTTONS_OK)
            alert_dialog.set_title(u"信息")
            alert_dialog.set_icon(app_info.app_icon)
            alert_dialog.set_markup(u"<b>Emacs server 尚未启动</b>\n请以 server 模式启动 emacs。")
            alert_dialog.run()
            alert_dialog.destroy()

    def __delete_note(self, widget):
        global settings, app_info
        notes_trash_dir = settings.get_trash_dir()
        alert_dialog = gtk.MessageDialog(parent = self.window, 
                                         type = gtk.MESSAGE_WARNING, 
                                         buttons = gtk.BUTTONS_YES_NO)
        alert_dialog.set_title(u"删除笔记")   
        alert_dialog.set_icon(app_info.app_icon)
        alert_dialog.set_markup(u"<b>删除笔记</b>\n您确定要删除此笔记吗？")
        response = alert_dialog.run()
        alert_dialog.destroy()
        if response == gtk.RESPONSE_YES:
            wiki_file = self.wiki.wiki_file
            os.system("mv " + wiki_file + " " + notes_trash_dir)
            wiki_list.update_wiki_list()

    def __history_prev(self, widget):
        if self.history.can_go_back():
            self.wiki = self.history.go_back()
            self.__view_wiki()
            self.history_prev_button.set_sensitive(self.history.can_go_back())
            self.history_next_button.set_sensitive(self.history.can_go_forward())

    def __history_next(self, widget):
        if self.history.can_go_forward():
            self.wiki = self.history.go_forward()
            self.__view_wiki()
            self.history_prev_button.set_sensitive(self.history.can_go_back())
            self.history_next_button.set_sensitive(self.history.can_go_forward())

    def __clear_history(self, widget):
        self.history.clear()
        self.history.push(self.wiki)
        self.history_prev_button.set_sensitive(False)
        self.history_next_button.set_sensitive(False)

    def __refresh(self, widget):
        self.wiki.update_cache()
        self.__view_wiki()
    
    def __update_wiki_list(self, widget):
        global wiki_list
        wiki_list.update_wiki_list()
        self.__set_jmptobtn_menu()

    def __on_menuitem_activate(self, widget, data):
        global settings
        html_cache_dir = settings.get_cache_dir()
        self.wiki = MuseWiki(data, html_cache_dir)
        self.history.push(self.wiki)
        self.history_prev_button.set_sensitive(self.history.can_go_back())
        self.history_next_button.set_sensitive(self.history.can_go_forward())
        self.__view_wiki()

    def __link_clicked(self, document, link):
        global settings
        html_cache_dir = settings.get_cache_dir()
        if urlparse(link)[0]:
            # Open in prefered browser in the case of an external link
            os.system("xdg-open " + link)
        else:
            # Internal link: generate the html file and view it
            muse_notes_dir = settings.get_notes_dir()
            muse_name_base = os.path.splitext(link)[0]
            wiki_file = os.path.join(muse_notes_dir, muse_name_base 
                                          + ".muse")
            self.history_prev_button.set_sensitive(True)
            self.history_next_button.set_sensitive(False)
            self.wiki = MuseWiki(wiki_file, html_cache_dir)
            self.history.push(self.wiki)
            self.__view_wiki()

    def __request_url(self, document, url, stream):
        base_dir = os.path.dirname(self.wiki.wiki_file)
        request_file = open(os.path.join(base_dir, url))
        stream.write(request_file.read())
        stream.close()
        request_file.close()

    def __set_jmptobtn_menu(self):
        global wiki_list
        notes_menu = gtk.Menu()
        for item in wiki_list.get_wiki_list():
            wiki = MuseWiki(item)
            notes_menu_item = gtk.MenuItem(wiki.get_title())
            notes_menu_item.connect("activate", self.__on_menuitem_activate, item)
            notes_menu.append(notes_menu_item)
        notes_menu.show_all()
        self.jumpto_button.set_menu(notes_menu)
        
    def __init__(self, filename):
        global settings, app_info
        html_cache_dir = settings.get_cache_dir()
        self.wiki = MuseWiki(filename, html_cache_dir)
        self.history = History()
        self.history.push(self.wiki)
        self.window = gtk.Window()
        # The toolbar
        toolbar = gtk.Toolbar()
        tool_button = gtk.ToolButton(gtk.STOCK_NEW)
        tool_button.connect("clicked", self.__new_note);
        toolbar.insert(tool_button, -1)
        tool_button = gtk.ToolButton(gtk.STOCK_EDIT)
        tool_button.connect("clicked", self.__edit_note);
        toolbar.insert(tool_button, -1)
        tool_button = gtk.ToolButton(gtk.STOCK_DELETE)
        tool_button.connect("clicked", self.__delete_note);
        toolbar.insert(tool_button, -1)
        tool_button = gtk.SeparatorToolItem()
        toolbar.insert(tool_button, -1)
        self.history_prev_button = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.history_prev_button.connect("clicked", self.__history_prev);
        self.history_prev_button.set_sensitive(False)
        toolbar.insert(self.history_prev_button, -1)
        self.history_next_button = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.history_next_button.connect("clicked", self.__history_next);
        self.history_next_button.set_sensitive(False)
        toolbar.insert(self.history_next_button, -1)
        tool_button = gtk.ToolButton(gtk.STOCK_CLEAR)
        tool_button.connect("clicked", self.__clear_history)
        toolbar.insert(tool_button, -1)
        tool_button = gtk.SeparatorToolItem()
        toolbar.insert(tool_button, -1)
        tool_button = gtk.ToolButton(gtk.STOCK_REFRESH)
        tool_button.connect("clicked", self.__refresh);
        toolbar.insert(tool_button, -1)
        self.jumpto_button = gtk.MenuToolButton(gtk.STOCK_JUMP_TO)
        self.jumpto_button.connect("clicked", self.__update_wiki_list)
        self.__set_jmptobtn_menu()
        toolbar.insert(self.jumpto_button, -1)
        handlebox = gtk.HandleBox()
        handlebox.add(toolbar)
        # The gtkhtml2 html viewer
        self.document = gtkhtml2.Document()
        self.document.connect("request_url", self.__request_url)
        self.document.connect("link_clicked", self.__link_clicked)
        view = gtkhtml2.View()
        view.set_document(self.document)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(view)
        # Pack them
        vbox = gtk.VBox()
        vbox.pack_start(handlebox, expand = False)
        vbox.pack_start(sw, expand = True)
        self.window.add(vbox)
        self.window.set_default_size(600, 500)
        self.window.set_icon(app_info.app_icon)
        view.grab_focus()
        
    def __view_wiki(self):
        title = self.wiki.get_title()
        html_buffer = self.wiki.get_html_content()
        self.document.clear()
        self.document.open_stream("text/html")
        self.document.write_stream(html_buffer)
        self.document.close_stream()
        self.window.set_title(title)

    def show(self):
        self.window.show_all()
        self.__view_wiki()
    
if __name__ == "__main__":
    print __doc__

