---
title: Usage of Makefile in Project Build Process
---
This document provides a detailed walkthrough of how the Makefile is used in the Sentry-Demo project. It explains the purpose of each command and how they contribute to the project's build process.

<SwmSnippet path="/Makefile" line="1">

---

# Makefile Overview

The Makefile begins by defining a few variables and targets. The `.PHONY` directive tells `make` that `all` and `develop` are not files. `PIP` and `WEBPACK` are set to specific command strings, and `POSTGRES_CONTAINER` is assigned a string value.

```
.PHONY: all
all: develop

PIP := python -m pip --disable-pip-version-check
WEBPACK := yarn build-acceptance
POSTGRES_CONTAINER := sentry_postgres
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="8">

---

# Freezing Requirements

The `freeze-requirements` target runs a Python script to freeze the project's dependencies. This is typically used to create a requirements.txt file that specifies exact package versions, ensuring consistent builds.

```
freeze-requirements:
	@python3 -S -m tools.freeze_requirements
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="11">

---

# Bootstrap

The `bootstrap` target provides instructions for setting up the development environment. It suggests running `devenv sync` to update the Sentry development environment.

```
bootstrap:
	@echo "devenv bootstrap is typically run on new machines."
	@echo "you probably want to run devenv sync to bring the"
	@echo "sentry dev environment up to date!"
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="16">

---

# Development Tasks

This section defines a series of targets for common development tasks, such as cleaning the environment, initializing the configuration, running dependent services, and installing development dependencies for JavaScript and Python. Each target runs a script with the corresponding name.

```
clean \
init-config \
run-dependent-services \
drop-db \
create-db \
apply-migrations \
reset-db \
node-version-check \
install-js-dev \
install-py-dev :
	@./scripts/do.sh $@
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="28">

---

# Develop

The `develop` target depends on `devenv-sync`, which runs the `devenv sync` command. This ensures that the development environment is up-to-date before starting the development process.

```
develop:
	devenv-sync

# This is to ensure devenv sync's only called once if the above
# macros are combined e.g. `make install-js-dev install-py-dev`
.PHONY: devenv-sync
devenv-sync:
	devenv sync
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="37">

---

# Building Assets and Upgrading Pip

These targets are for building platform assets, displaying help for `direnv`, and upgrading `pip`. They all run scripts with the corresponding names.

```
build-platform-assets \
direnv-help \
upgrade-pip :
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="42">

---

# Building JavaScript PO

The `build-js-po` target depends on `node-version-check`. It creates a build directory, removes the babel-loader cache, and runs the `yarn build-acceptance` command with `SENTRY_EXTRACT_TRANSLATIONS=1`.

```
build-js-po: node-version-check
	mkdir -p build
	rm -rf node_modules/.cache/babel-loader
	SENTRY_EXTRACT_TRANSLATIONS=1 $(WEBPACK)
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="47">

---

# Building Spectacular Docs

The `build-spectacular-docs` target builds the drf-spectacular openapi spec, which combines with deprecated docs.

```
build-spectacular-docs:
	@echo "--> Building drf-spectacular openapi spec (combines with deprecated docs)"
	@OPENAPIGENERATE=1 sentry django spectacular --file tests/apidocs/openapi-spectacular.json --format openapi-json --validate --fail-on-warn
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="51">

---

# Building Deprecated Docs

The `build-deprecated-docs` target builds the deprecated openapi spec from json files.

```
build-deprecated-docs:
	@echo "--> Building deprecated openapi spec from json files"
	yarn build-deprecated-docs
```

---

</SwmSnippet>

<SwmSnippet path="/Makefile" line="55">

---

# Building API Docs

The `build-api-docs` target depends on `build-deprecated-docs` and `build-spectacular-docs`. It dereferences the json schema for ease of use.

```
build-api-docs: build-deprecated-docs build-spectacular-docs
	@echo "--> Dereference the json schema for ease of use"
	yarn deref-api-docs
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="general-build-tool"><sup>Powered by [Swimm](/)</sup></SwmMeta>
