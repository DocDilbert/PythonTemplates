test:
	python -m pytest unit_tests

html: 
	$(MAKE) -C ./docs html

clean:
	rm -f ./qttool/ui/ui_mainwindow.py
	$(MAKE) -C ./docs clean

ui:
	pyuic5 ./qttool/ui/mainwindow.ui -o ./qttool/ui/ui_mainwindow.py
.PHONY: test html clean ui
