caja:
	cat Maildir.py > MaildirCaja.py

nemo:
	sed 's%caja%nemo%g' Maildir.py | sed 's%Caja%Nemo%g' > MaildirNemo.py

nautilus:
	sed 's%caja%nautilus%g' Maildir.py | sed 's%Caja%Nautilus%g' > MaildirNautilus.py

install-caja: caja
	mkdir -p $$XDG_DATA_HOME/caja-python/extensions/
	cp MaildirCaja.py $$XDG_DATA_HOME/caja-python/extensions/

install-nemo: nemo
	mkdir -p $$XDG_DATA_HOME/nemo-python/extensions/
	cp MaildirNemo.py $$XDG_DATA_HOME/nemo-python/extensions/

install-nautilus: nautilus
	mkdir -p $$XDG_DATA_HOME/nautilus-python/extensions/
	cp MaildirNautilus.py $$XDG_DATA_HOME/nautilus-python/extensions/

install-all: install-caja install-nemo install-nautilus

all: caja nemo nautilus
