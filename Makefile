# Simple makefile
#
# Author: YangZhang <zyang@lsec.cc.ac.cn>
# Last updated: 2008-10-27 17:41:38
#

install:
	/usr/bin/install muse-icon.py /usr/local/muse-icon/muse-icon.py
	ln -s /usr/local/muse-icon/muse-icon.py /usr/local/bin/muse-icon
