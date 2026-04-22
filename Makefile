.PHONY: all build test test-shell build-test install-act check-act run-act-tests

################################################################################
# GLOBALS
################################################################################

# docker build options
CURRENTDIR := $(PWD)
DCKR_NOCACHE ?= false
DCKR_PULL ?= true
DCKR_NOCACHE ?= false
DCKRTTY := $(if $(filter true,$(NOTTY)),-i,-it)
USE_VOL ?= true
USE_USR ?= true
TESTVOL = $(if $(filter true,$(USE_VOL)),-v ${CURRENTDIR}:/home/jovyan,)
DCKRUSR = $(if $(filter true,$(USE_USR)),--user $(shell id -u):$(shell id -g),)
DCKRTST = docker run --rm ${DCKRUSR} --entrypoint "" ${TESTVOL}
DCKRIMG_BASE ?= ghcr.io/diogenesanalytics/scipy-notebook:master
DCKRIMG_TESTS ?= $(DCKRIMG_BASE)-tests

# act config
ACT_BIN_DIR ?= ./bin
ACT         ?= $(ACT_BIN_DIR)/act
ACT_VERSION ?= latest


# Define the docker build command with optional --no-cache
define DOCKER_BUILD
	docker build -t $1 . --load --target $2 \
	  $(if $(filter true,$(DCKR_NOCACHE)),--no-cache)
endef

# Function to conditionally pull or build the docker image
define DOCKER_PULL_OR_BUILD
	$(if $(filter true,$(DCKR_PULL)), \
	  docker pull $1 || (echo "Pull failed. Building Docker image for $1..." && \
	  $(call DOCKER_BUILD,$1,$2)), $(call DOCKER_BUILD,$1,$2))
endef

################################################################################
# DEFAULT
################################################################################

all: build-base

################################################################################
# BUILD
################################################################################

# build jupyter docker image with conditional pull and build
build-base:
	@ echo "Building Jupyter Docker image..."
	@ $(call DOCKER_PULL_OR_BUILD,${DCKRIMG_BASE},base)

# build testing docker image with conditional pull and build
build-tests:
	@ echo "Building Test Docker image..."
	@ $(call DOCKER_PULL_OR_BUILD,${DCKRIMG_TESTS},test)

################################################################################
# TESTING (DOCKER-BASED)
################################################################################

# run linters
lint: isort black flake8 mypy

# run full testing suite
tests: pytest lint

# run pytest in docker container
pytest:
	@ echo "==> Running pytest..."
	@ ${DCKRTST} ${DCKRIMG_TESTS} pytest tests/

# run isort in docker container
isort:
	@ echo "==> Running isort..."
	@ ${DCKRTST} ${DCKRIMG_TESTS} isort tests/

# run black in docker container
black:
	@ echo "==> Running black..."
	@ ${DCKRTST} ${DCKRIMG_TESTS} black tests/

# run flake8 in docker container
flake8:
	@ echo "==> Running flake8..."
	@ ${DCKRTST} ${DCKRIMG_TESTS} flake8 tests/

# run mypy in docker container
mypy:
	@ echo "==> Running mypy..."
	@ ${DCKRTST} ${DCKRIMG_TESTS} mypy --ignore-missing-imports tests/


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
	@if [ -x "$(ACT)" ]; then \
		echo "✅ act found at $(ACT)"; \
	elif command -v act >/dev/null 2>&1; then \
		echo "✅ act found in PATH"; \
	else \
		echo "❌ act is not installed. Run: make install-act"; \
		exit 1; \
	fi

run-act-tests: check-act
	@echo "Running GitHub Actions locally..."
	@$(ACT) push -j build $(ARGS)
