update:
	 python -m cppstate config_sol.json

compile:
	 $(MAKE) -C ./autogen all
	
run: compile
	./autogen/main.exe

doc: 
	$(MAKE) -C ./autogen doc

clean:
	rm -r autogen

.PHONY: test html clean ui
