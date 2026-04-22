.PHONY: all build install-act check-act run-act-tests

################################################################################
# GLOBALS
################################################################################

DCTNR := $(notdir $(PWD))

# docker build options
DCKR_NOCACHE ?= false

# image name
DCKRIMG_BASE ?= ghcr.io/diogenesanalytics/$(DCTNR):master

# optional flags
NOCACHE_FLAG := $(if $(filter true,$(DCKR_NOCACHE)),--no-cache,)

# act config
ACT_BIN_DIR ?= ./bin
ACT         ?= $(ACT_BIN_DIR)/act
ACT_VERSION ?= latest

################################################################################
# DEFAULT
################################################################################

all: build

################################################################################
# DOCKER BUILD
################################################################################

build:
	@echo "Building reproducible Jupyter image..."
	@docker build \
		--pull \
		-t $(DCKRIMG_BASE) \
		$(NOCACHE_FLAG) \
		.

################################################################################
# GITHUB ACTIONS (LOCAL VIA ACT)
################################################################################

install-act:
	@echo "Installing act locally..."
	@mkdir -p $(ACT_BIN_DIR)
	@curl --proto '=https' --tlsv1.2 -sSf \
	  https://raw.githubusercontent.com/nektos/act/master/install.sh | \
	  bash -s -- -b $(ACT_BIN_DIR) $(ACT_VERSION)
	@echo "Installed act at $(ACT)"

check-act:
	@command -v act >/dev/null 2>&1 || \
	{ echo "❌ act is not installed. Run: make install-act"; exit 1; }
	@echo "✅ act is installed"

run-act-tests: check-act
	@echo "Running GitHub Actions locally..."
	act -j run-tests $(ARGS)
