test:
	python -m pytest unit_tests

html: 
	$(MAKE) -C ./docs html

clean:
	$(MAKE) -C ./docs clean

ui:
	pyuic5 ./qttool/mainWindow.ui -o ./qttool/ui_mainWindow.py
.PHONY: test html clean ui
