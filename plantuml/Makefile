JAVA = java
PLANTUML_JAR = c:\Dev\PlantUml\plantuml.jar

PLANTUML = @$(JAVA) -Dapple.awt.UIElement=true -jar $(PLANTUML_JAR) -progress -charset UTF-8
DIR_GUARD = @mkdir -p $(@D)
OUT_DIR = diags

DIAGS = 
DIAGS += class_ref1
DIAGS += class_ref2
DIAGS += class_ref3
DIAGS += EtherCatImplementation
DIAGS += ProfiNetImplementation
DIAGS += GeneralComManager

DIAGS_PNG = $(foreach diag,$(DIAGS),$(OUT_DIR)/$(diag).png)
DIAGS_SVG = $(foreach diag,$(DIAGS),$(OUT_DIR)/$(diag).svg)

all: $(DIAGS_PNG) $(DIAGS_SVG)

$(OUT_DIR)/%.png: %.wsd 
	$(DIR_GUARD)
	@echo Generating $@ ...
	$(PLANTUML) $< -o $(OUT_DIR)
	@echo

$(OUT_DIR)/%.svg: %.wsd 
	$(DIR_GUARD)
	@echo Generating $@ ..,
	$(PLANTUML) $< -tsvg -o $(OUT_DIR)
	@echo

.PHONY: clean archive

clean:
	rm -rf $(OUT_DIR)

archive:
	tar -cf ../$(notdir $(CURDIR)).tar *