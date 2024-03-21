DOFUSINVOKER = D://Dofus//DofusInvoker.swf
PYDOFUS_DIR = D://botdev//pydofus2
PYD2BOT_DIR = D://botdev//pyd2bot
VENV_DIR = D://botdev//.venv
FFDEC = $(CURDIR)/FFDec/ffdec.bat
DOFUS_SRC_DIR = $(CURDIR)/protocolBuilder/sources
VENVACTIVATE = $(VENV_DIR)/Scripts/activate
SELECTCLASS = com.ankamagames.dofus.BuildInfos,com.ankamagames.dofus.network.++,com.ankamagames.jerakine.network.++
PYDOFUS_BINARY_DATA_DIR = $(PYDOFUS_DIR)/pydofus2/binaryData
# Dist and build paths
PYD2BOT_BUILD_DIR = $(CURDIR)/pyd2botBuild
PYD2BOT_BUILDENV = $(PYD2BOT_BUILD_DIR)/.buildEnv
SNIFFER_APP_DIR = $(CURDIR)/sniffer
PD2B_THRSERVER_DIR = $(PYD2BOT_DIR)/pyd2bot/thriftServer
PYD2BOT_THRIFT_SERVICE = $(PD2B_THRSERVER_DIR)/pyd2botService.thrift
# (old)
GRINDER_DIR = D://botdev/Grinder
PYD2BOT_DIST_DIR = $(GRINDER_DIR)/dist_electron/pyd2bot/
GRINDER_THRIFT_DIR = $(GRINDER_DIR)/src/services

.ONESHELL:
.PHONY: setup

paths:
	@source "$(CURDIR)/spinner.sh"
	echo "$(PYDOFUS_DIR)" >> $(VENV_DIR)/pydofus2.pth
	echo "$(PYD2BOT_DIR)" >> $(VENV_DIR)/pyd2bot.pth

venv:
	@source "$(CURDIR)/spinner.sh"
	@python -m venv $(VENV_DIR) & spinner "Creating dev env"
	@source $(VENV_DIR)/Scripts/activate & spinner "Activating dev env"
	@pip install --upgrade pip --quiet\
	&& pip install --upgrade setuptools --quiet & spinner "Upgrading pip and setuptools"

deps:
	@source "$(CURDIR)/spinner.sh"
	@pip install -r $(PYDOFUS_DIR)/requirements.txt --quiet & spinner "Installing pydofus2 requirements"
	@pip install -r $(PYD2BOT_DIR)/requirements.txt --quiet & spinner "Installing pyd2bot requirements"
	@pip install -r $(SNIFFER_APP_DIR)/requirements.txt & spinner "Installing snifferApp requirements"
	@tput cnorm
.ONESHELL:
setup-env: venv paths deps


setupSniffer:
	cd sniffer
	python -m venv $(SNIFFER_APP_DIR)/.devVenv
	source $(SNIFFER_APP_DIR)/.devVenv/Scripts/activate
	pip install --upgrade pip
	pip install --upgrade setuptools
	echo "$(PYDOFUS_DIR)" >> $(SNIFFER_APP_DIR)/.devVenv/pydofus2.pth
	echo "$(PYD2BOT_DIR)" >> $(SNIFFER_APP_DIR)/.devVenv/pyd2bot.pth
	echo $(CURDIR) >> $(SNIFFER_APP_DIR)/.devVenv/pyd2botDevTools.pth
	pip install -r $(PYDOFUS_DIR)/requirements.txt --quiet
	pip install -r $(PYD2BOT_DIR)/requirements.txt --quiet
	pip install -r $(SNIFFER_APP_DIR)/requirements.txt
	
sniff:
	@source $(VENV_DIR)/Scripts/activate
	@python $(SNIFFER_APP_DIR)/network/DofusSniffer.py

update: decompile gen-protocol gen-msgClasses gen-msgShuffle extract-keys unpack-maps

decompile:
	@$(FFDEC) -config parallelSpeedUp=true -selectclass $(SELECTCLASS) -export script $(DOFUS_SRC_DIR) $(DOFUSINVOKER)

decompile-all:
	@$(FFDEC) -config parallelSpeedUp=true -timeout 14400 -exportTimeout 14400 -exportFileTimeout 14400 -export script,binaryData $(CURDIR)/../../d2sources $(DOFUSINVOKER)

extract-keys:
	@$(FFDEC) -config parallelSpeedUp=true -export binaryData $(PYDOFUS_BINARY_DATA_DIR) $(DOFUSINVOKER)

gen-protocol:
	@source $(VENV_DIR)/Scripts/activate
	@echo "Generating protocol..."
	@python protocolBuilder/protocolParser.py $(DOFUS_SRC_DIR)
	@echo "Protocol generated"

gen-msgClasses:
	@source $(VENV_DIR)/Scripts/activate
	@pip install jinja2
	@pip install tqdm
	@echo "Generating msgClasses..."
	@python protocolBuilder/exportClasses.py $(PYDOFUS_DIR)
	@echo "msgClasses generated"

gen-msgShuffle:
	@source $(VENV_DIR)/Scripts/activate
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

gen-thrift:
	@cd $(PD2B_THRSERVER_DIR)
	@./thrift-0.16.0.exe -r --gen js:node,ts,es6,with_ns $(PYD2BOT_THRIFT_SERVICE) && rm -rf gen-nodejs
	@./thrift-0.16.0.exe -r --gen py $(PYD2BOT_THRIFT_SERVICE) \
	&& cp -r gen-py/* $(PD2B_THRSERVER_DIR) \
	&& rm -rf gen-py

black:
	@source $(VENV_DIR)/Scripts/activate
	@pip install black
	@black $(PYDOFUS_DIR)/**/*/*.py
