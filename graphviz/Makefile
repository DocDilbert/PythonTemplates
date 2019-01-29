DIR_GUARD = @mkdir -p $(@D)
OUT_DIR = graphs

GRAPHS = $(OUT_DIR)/graph1.pdf
GRAPHS += $(OUT_DIR)/graph2.pdf
all: $(GRAPHS)

$(OUT_DIR)/graph1.pdf: graph1.dot 
	$(DIR_GUARD)
	dot -Tpdf $< -o $@

$(OUT_DIR)/graph2.pdf: graph2.dot 
	$(DIR_GUARD)
	dot -Tpdf $< -o $@

.PHONY: clean

clean:
	rm -rf graphs