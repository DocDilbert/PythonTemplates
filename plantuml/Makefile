DIR_GUARD = @mkdir -p $(@D)
OUT_DIR = diags

DIAG_PNG = 
DIAG_PNG += $(OUT_DIR)/class.png

DIAG_SVG = 
DIAG_SVG += $(OUT_DIR)/class.svg



all: $(DIAG_PNG) $(DIAG_SVG)

$(OUT_DIR)/%.png: %.wsd 
	$(DIR_GUARD)
	plantuml $< -o $(OUT_DIR)

$(OUT_DIR)/%.svg: %.wsd 
	$(DIR_GUARD)
	plantuml $< -tsvg -o $(OUT_DIR)

.PHONY: clean

clean:
	rm -rf $(OUT_DIR)