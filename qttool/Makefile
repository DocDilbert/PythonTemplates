test:
	python -m pytest unit_tests

html: 
	$(MAKE) -C ./docs html

clean:
	$(MAKE) -C ./docs clean

ui:
	pyuic5 ./qttool/ui/mainwindow.ui -o ./qttool/ui/ui_mainwindow.py
.PHONY: test html clean ui
