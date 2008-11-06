#!/usr/bin/env python
#-*- coding: utf-8 -*-
#


import os
import re

class MuseWiki():
    "Wrap Emacs/Muse wiki"
    def __init__(self, wiki_file, cache_dir = "/tmp/Muse/"):
        self.wiki_file = wiki_file
        self.__cache_dir__ = os.path.abspath(os.path.expanduser(cache_dir))
    
    def __check_cache__(self):
        html_file = os.path.splitext(os.path.basename(self.wiki_file))[0] + ".html"
        html_file = os.path.join(self.__cache_dir__, html_file)
        if not os.path.exists(html_file):
            self.update_cache()
        
    def update_cache(self):
        command = "emacs"
        argument = " --batch --eval "
        elisp_script = "\"(progn (require 'muse-html) (muse-publish-file \\\"" \
            + self.wiki_file + "\\\" \\\"html\\\" \\\""  \
            + self.__cache_dir__ + "\\\" " + " 'force))\""
        os.system(command + argument + elisp_script)
        
    def get_html_content(self):
        self.__check_cache__()
        html_base_filename = os.path.splitext(os.path.basename(self.wiki_file))[0]
        html_file_name = os.path.join(self.__cache_dir__, html_base_filename + ".html")
        html_file = open(html_file_name)
        html_buffer = html_file.readlines()
        html_file.close()
        # filter out the title line to avoid mass-up of display
        title_line = re.compile("^[^<]*<title>[^<]*</title>.*$")
        for index in range(len(html_buffer)):
            result = title_line.search(html_buffer[index])
            if result:
                del(html_buffer[index])
                break
        result = "".join(html_buffer)
        return result       

    def get_title(self):
        # two patterns of title: explict #title line and level one header
        title_pattern_0 = re.compile("^[ ]*#title[ ]*(.*)[ ]*$")
        title_pattern_1 = re.compile("^[ ]*\*[ ]+(.*)[ ]*$")
        
        in_file = open(self.wiki_file)
        lines_buffer = in_file.readlines()
        in_file.close()
        for line in lines_buffer:
            result = title_pattern_0.match(line)
            if result:
                return result.group(1)
            result = title_pattern_1.match(line)
            if result:
                return result.group(1)

        return os.path.splitext(os.path.basename(self.wiki_file))[0]
    
if __name__ == "__main__":
    pass


