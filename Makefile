# Simple makefile
#
# Author: YangZhang <zyang@lsec.cc.ac.cn>
# Last updated: 2008-10-27 17:41:38
#

INSTALL = /usr/bin/install

APP_MAIN = main.py
OBJECTS = ${APP_MAIN} ui_viewer.py ui_statusicon.py settings.py \
		  muse_helper.py app_globals.py
		  
DEST_DIR = /usr/local
APP_NAME = muse-icon

all:

install:
	if [ ! -d ${DEST_DIR}/${APP_NAME} ]; then \
		mkdir -p ${DEST_DIR}/${APP_NAME}; \
	fi
	${INSTALL} ${OBJECTS} ${DEST_DIR}/${APP_NAME}
	chmod a+x ${DEST_DIR}/${APP_NAME}/${APP_MAIN}
	ln -sf ${DEST_DIR}/${APP_NAME}/${APP_MAIN} ${DEST_DIR}/bin/${APP_NAME}

clean:
	-rm -f *.pyc
