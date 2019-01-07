test:
	python -m pytest unit_tests

html: 
	$(MAKE) -C ./docs html

clean:
	$(MAKE) -C ./docs clean

ui:
	pyuic5 ./autocomment/ui/mainwindow.ui -o ./autocomment/ui/ui_mainwindow.py
.PHONY: test html clean ui
