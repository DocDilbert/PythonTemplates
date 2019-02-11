# set visible compiler options
V?=0
Q=@
ifeq ($(V),1)
 Q=
endif

MAKEFLAGS += --no-builtin-rules

# Suffixes
.SUFFIXES:                          # Delete the default suffixes
.SUFFIXES: .S .c .cpp .h .o .d      # Define our suffix list

JAVA = java
PLANTUML_JAR = C:/Dev/PlantUml/plantuml.jar

PLANTUML = @$(JAVA) -Dapple.awt.UIElement=true -jar $(PLANTUML_JAR)

dir_guard = @mkdir -p $(@D)
OUT_O_DIR = objs

OBJECTS = 
OBJECTS += $(OUT_O_DIR)/tests.o
OBJECTS += $(OUT_O_DIR)/Client.o
OBJECTS += $(OUT_O_DIR)/WeatherData.o

INCLUDES =
INCLUDES += -I../libs/catch/
INCLUDES += -I./Observer

VPATH += ./Observer
all: tests.exe

tests.exe: $(OBJECTS)
	g++ -o tests.exe $(OBJECTS)

$(OUT_O_DIR)/%.o: %.cpp
	$(dir_guard)
	g++ -O0 $(INCLUDES) -c $< -o $@

clean:
	rm -rf $(OUT_O_DIR)
	rm -f tests.exe

doc: StateMachine.wsd
	$(PLANTUML) StateMachine.wsd

.PHONY: clean 