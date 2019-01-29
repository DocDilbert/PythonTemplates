dir_guard = @mkdir -p $(@D)
OUT_DIR = graphs

$(OUT_DIR)/graph1.pdf: graph1.dot 
	$(dir_guard)
	dot -Tpdf $< -o $@