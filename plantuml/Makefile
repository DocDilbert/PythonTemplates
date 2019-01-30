
JAVA = java
PLANTUML_POS = /usr/local/Cellar/plantuml/1.2019.0/libexec/plantuml.jar

PLANTUML = $(JAVA) -Dapple.awt.UIElement=true -jar $(PLANTUML_POS)
DIR_GUARD = @mkdir -p $(@D)
OUT_DIR = diags

DIAG_PNG = 
DIAG_PNG += $(OUT_DIR)/class_ref1.png
DIAG_PNG += $(OUT_DIR)/class_ref2.png
DIAG_PNG += $(OUT_DIR)/class_ref3.png
DIAG_PNG += $(OUT_DIR)/GeneralComManager.png

DIAG_SVG = 
DIAG_SVG += $(OUT_DIR)/class_ref1.svg
DIAG_SVG += $(OUT_DIR)/class_ref2.svg
DIAG_SVG += $(OUT_DIR)/class_ref3.svg
DIAG_SVG += $(OUT_DIR)/GeneralComManager.svg


all: $(DIAG_PNG) $(DIAG_SVG)

$(OUT_DIR)/%.png: %.wsd 
	$(DIR_GUARD)
	$(PLANTUML) $< -o $(OUT_DIR)

$(OUT_DIR)/%.svg: %.wsd 
	$(DIR_GUARD)
	$(PLANTUML) $< -tsvg -o $(OUT_DIR)

.PHONY: clean

clean:
	rm -rf $(OUT_DIR)