update:
	 python -m generate

compile:
	 $(MAKE) -C ./autogen all
	
run: compile
	./autogen/main.exe

clean:
	rm -r autogen

.PHONY: test html clean ui
