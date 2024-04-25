LIBFOLDER = /usr/local/lib/navigator
BINFILE = /usr/local/lib/navigator/nav.py
BINLINK = /usr/local/bin/nav
CONFFILE = ~/.navconf

.PHONY: uninstall

install: uninstall
	activate-global-python-argcomplete
	cp -R . $(LIBFOLDER)
	sed -i '' '1s|^.*$$|#!/usr/local/lib/navigator/navenv/bin/python|' $(BINFILE)
	ln -s $(BINFILE) $(BINLINK)
	eval "$$(register-python-argcomplete nav)"

full-uninstall: uninstall
	rm $(CONFFILE)

uninstall: 
	rm -rf $(LIBFOLDER)
	rm -rf $(BINLINK)

help: 
	@echo "Installs/uninstalls navigator in the binaries."
	@echo "Usage: make [install|uninstall|full-uninstall]"