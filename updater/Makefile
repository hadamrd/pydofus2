
ifeq ($(OS),Windows_NT)
	DOFUS_HOME := $(subst \,/,$(DOFUS_HOME))
	PYBOTDEV_HOME := $(subst \,/,$(PYBOTDEV_HOME))
endif
DOFUSINVOKER = $(DOFUS_HOME)/DofusInvoker.swf
PYDOFUS_DIR = $(PYBOTDEV_HOME)/pydofus2
PYD2BOT_DIR = $(PYBOTDEV_HOME)/pyd2bot
VENV_DIR = $(PYBOTDEV_HOME)/.venv
FFDEC = $(CURDIR)/FFDec/ffdec.bat
DOFUS_SRC_DIR = $(CURDIR)/protocolBuilder/sources
VENVACTIVATE = $(VENV_DIR)/Scripts/activate
SELECTCLASS = com.ankamagames.dofus.BuildInfos,com.ankamagames.dofus.network.++,com.ankamagames.jerakine.network.++
PYDOFUS_BINARY_DATA_DIR = $(PYDOFUS_DIR)/pydofus2/binaryData
# Dist and build paths
PYD2BOT_BUILD_DIR = $(CURDIR)/pyd2botBuild
PYD2BOT_BUILDENV = $(PYD2BOT_BUILD_DIR)/.buildEnv
SNIFFER_APP_DIR = $(PYDOFUS_DIR)/sniffer/app
PYD2BOT_APP_DIR = $(PYD2BOT_DIR)/app

venv:
	@source "$(CURDIR)/spinner.sh"
	@python -m venv $(VENV_DIR) & spinner "Creating dev env"
	@source $(VENV_DIR)/Scripts/activate & spinner "Activating dev env"
	@pip install --upgrade pip --quiet\
	&& pip install --upgrade setuptools --quiet & spinner "Upgrading pip and setuptools"
	
sniff:
	@source $(VENVACTIVATE)
	@python $(SNIFFER_APP_DIR)/app.py

serve:
	@source $(VENVACTIVATE)
	@python $(PYD2BOT_APP_DIR)/app.py

update: decompile gen-protocol gen-msgClasses gen-msgShuffle extract-keys unpack-maps

decompile:
	@$(FFDEC) -config parallelSpeedUp=true -selectclass $(SELECTCLASS) -export script $(DOFUS_SRC_DIR) $(DOFUSINVOKER)

decompile-all:
	@$(FFDEC) -config parallelSpeedUp=true -timeout 14400 -exportTimeout 14400 -exportFileTimeout 14400 -export script,binaryData $(CURDIR)/../../d2sources $(DOFUSINVOKER)

extract-keys:
	@$(FFDEC) -config parallelSpeedUp=true -export binaryData $(PYDOFUS_BINARY_DATA_DIR) $(DOFUSINVOKER)

gen-protocol:
	@source $(VENVACTIVATE)
	@echo "Generating protocol..."
	@python protocolBuilder/protocolParser.py $(DOFUS_SRC_DIR)
	@echo "Protocol generated"

gen-msgClasses:
	@source $(VENVACTIVATE)
	@pip install jinja2
	@pip install tqdm
	@echo "Generating msgClasses..."
	@python protocolBuilder/exportClasses.py $(PYDOFUS_DIR)
	@echo "msgClasses generated"

gen-msgShuffle:
	@source $(VENVACTIVATE)
	@$(FFDEC) -config parallelSpeedUp=true -selectclass com.ankamagames.dofus.network.MessageReceiver -export script $(DOFUS_SRC_DIR) $(DOFUSINVOKER)
	@python protocolBuilder/extractMsgShuffle.py $(DOFUS_SRC_DIR)/scripts/com/ankamagames/dofus/network/MessageReceiver.as
	@echo "msgShuffle generated"

unpack-maps:
	@source $(VENVACTIVATE)
	@echo "Unpacking maps..."
	@python scripts/unpack_maps.py
	@echo "Maps unpacked"

build-venv:
	@python -m venv .buildEnv & spinner "Creating virtual environment"
	@source .buildEnv/Scripts/activate
	@python -m pip install --upgrade pip --quiet & spinner "Upgrading pip" 
	@pip install wheel --quiet & spinner "Installing wheel"

lint:
	@tput civis
	@source "$(CURDIR)/spinner.sh"
	@cd $(PYD2BOT_BUILD_DIR)
	@source .buildEnv/Scripts/activate
	@pip install autoflake
	@autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive $(PYD2BOT_DIR) & spinner "Cleaning pyd2bot with autoflake"
	@autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive $(PYDOFUS_DIR) & spinner "Cleaning pydofus2 with autoflake"
	@pip install black --quiet & spinner "Installing black"
	@black -l 100  $(PYDOFUS_DIR)/**/*/*.py & spinner "formating pydofus2 files lines with black"
	@black -l 100  $(PYD2BOT_DIR)/**/*/*.py & spinner "formating pyd2bot files lines with black"
	@black $(PYDOFUS_DIR)/**/*/*.py & spinner "formating pydofus2 with black"
	@black $(PYD2BOT_DIR)/**/*/*.py & spinner "formating pyd2bot with black"
	
bdist:
	@bstart_time=$SECONDS
	@tput civis
	@source "$(CURDIR)/spinner.sh"
	@cd $(PYD2BOT_BUILD_DIR)
	@python -m venv .buildEnv & spinner "Creating virtual environment"
	@source .buildEnv/Scripts/activate
	@python -m pip install --upgrade pip --quiet & spinner "Upgrading pip" 
	@pip install wheel --quiet & spinner "Installing wheel"
	@pip install $(PYDOFUS_DIR)
	@pip install $(PYD2BOT_DIR)
	@pip install cx_Freeze
	@python build.py build
	@rm -r $(PYD2BOT_DIST_DIR)* & spinner "Create and clean dist directory" 
	@cp -a build/exe.win-amd64-3.9/* $(PYD2BOT_DIST_DIR) & spinner "Copying pyd2bot to dist"
	@tput cnorm
	@echo "Build completed in $$((SECONDS - bstart_time)) seconds"

black:
	@source $(VENV_DIR)/Scripts/activate
	@pip install black
	@black $(PYDOFUS_DIR)/**/*/*.py
