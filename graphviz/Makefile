DIR_GUARD = @mkdir -p $(@D)
OUT_DIR = graphs

GRAPHS = $(OUT_DIR)/graph1.pdf
GRAPHS += $(OUT_DIR)/graph2.pdf
GRAPHS += $(OUT_DIR)/graph3.pdf

all: $(GRAPHS)

$(OUT_DIR)/%.pdf: %.dot 
	$(DIR_GUARD)
	dot -Tpdf $< -o $@

.PHONY: clean

clean:
	rm -rf graphs