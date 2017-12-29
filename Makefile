PACKAGE_VERSION=0.0.1
prefix=/usr

all:

install:
	install -d -m 0755 "$(DESTDIR)/$(prefix)/sbin"
	install -m 0755 webwin "$(DESTDIR)/$(prefix)/sbin"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/lib/webwin"
	cp -r lib/* "$(DESTDIR)/$(prefix)/lib/webwin"
	find "$(DESTDIR)/$(prefix)/lib/webwin" -path "$(DESTDIR)/$(prefix)/lib/webwin/plugins" -prune -o -type f | xargs chmod 644
	find "$(DESTDIR)/$(prefix)/lib/webwin" -path "$(DESTDIR)/$(prefix)/lib/webwin/plugins" -prune -o -type d | xargs chmod 755

	install -d -m 0755 "$(DESTDIR)/$(prefix)/lib/systemd/system"
	install -m 0644 data/webwin.service "$(DESTDIR)/$(prefix)/lib/systemd/system"

uninstall:
	rm -f "$(DESTDIR)/$(prefix)/sbin/webwin"
	rm -f "$(DESTDIR)/$(prefix)/lib/systemd/system/webwin.service"
	rm -rf "$(DESTDIR)/$(prefix)/lib/webwin"

.PHONY: all install uninstall
