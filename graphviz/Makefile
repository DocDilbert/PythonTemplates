DIR_GUARD = @mkdir -p $(@D)
OUT_DIR = graphs

GRAPHS_PDF = $(OUT_DIR)/graph1.pdf
GRAPHS_PDF += $(OUT_DIR)/graph2.pdf
GRAPHS_PDF += $(OUT_DIR)/graph3.pdf
GRAPHS_PDF += $(OUT_DIR)/graph4.pdf
GRAPHS_PDF += $(OUT_DIR)/graph5.pdf
GRAPHS_PDF += $(OUT_DIR)/graph6.pdf
GRAPHS_PDF += $(OUT_DIR)/power_stage_release.pdf

GRAPHS_PNG += $(OUT_DIR)/power_stage_release.png

all: $(GRAPHS_PDF) $(GRAPHS_PNG)

$(OUT_DIR)/%.pdf: %.dot 
	$(DIR_GUARD)
	dot -Tpdf $< -o $@
	
$(OUT_DIR)/%.png: %.dot 
	$(DIR_GUARD)
	dot -Tpng $< -o $@

.PHONY: clean

clean:
	rm -rf graphs