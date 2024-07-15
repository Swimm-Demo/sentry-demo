---
title: >-
  product-Importing Configurations and Administrator Accounts into a Sentry
  Instance
---
This document will cover the process of importing configurations and administrator accounts into a Sentry instance. We'll cover:

1. The initiation of the import process
2. The import of all models required to globally configure and administrate a Sentry instance
3. The core of the import process
4. Writing the imported models into the database
5. Resolving organization slugs and creating slug reservations
6. Writing a single model
7. Importing a model
8. Writing the model instance to the database
9. Saving the event after normalizing and processing it.

Technical document: <SwmLink doc-title="Understanding the import_config Function">[Understanding the import_config Function](/.swm/understanding-the-import_config-function.uyvlp2xx.sw.md)</SwmLink>

# Initiation of the Import Process

The import process is initiated by the `import_config` function. This function takes several parameters including the source file, decryption keys, and various flags. It then calls the `import_in_config_scope` function, passing along these parameters.

# Import of All Models

The `import_in_config_scope` function is responsible for performing an import in the `Config` scope. This means it imports all models required to globally configure and administrate a Sentry instance from the provided source file. It calls the `_import` function to perform the actual import.

# Core of the Import Process

The `_import` function is the core of the import process. It reads the content from the source file, parses it into models, and then writes these models into the database. It also resolves organization slugs and creates slug reservations.

# Writing the Imported Models into the Database

The `do_writes` function is responsible for writing the imported models into the database. It iterates over the models and calls the `do_write` function for each one.

# Resolving Organization Slugs and Creating Slug Reservations

The `resolve_org_slugs_from_pk_map` function resolves slugs for all imported organization models and reconciles their slug globally by issuing a slug update. It calls the `bulk_create_organization_slugs` function to create slug reservations.

# Writing a Single Model

The `do_write` function is responsible for writing a single model. It first checks if the model has any dependencies. If not, it returns. Otherwise, it retrieves the model's dependencies and the appropriate importer for the model. It then calls the `import_by_model` function with the necessary parameters.

# Importing a Model

The `import_by_model` function is responsible for importing a model. It first checks if the model can be imported based on its name, scope, and flags. If the model can be imported, it deserializes the JSON data and writes the model instance to the database. If the model instance already exists, it updates the existing instance. If the model instance does not exist, it creates a new instance.

# Writing the Model Instance to the Database

The `write_relocation_import` function is responsible for writing the model instance to the database. It first checks if the model instance has a unique set of fields that could potentially cause collisions. If the model instance has a unique set of fields, it checks if an existing model instance with the same unique set of fields already exists. If an existing model instance exists, it either reuses the existing data or overwrites the existing data based on the flags. If an existing model instance does not exist, it writes the model instance as usual.

# Saving the Event After Normalizing and Processing It

The `save` function is responsible for saving the event after normalizing and processing it. It first checks if the event has been normalized. If not, it normalizes the event. It then writes the event to the eventstream. If the event is a transaction, it saves the transaction event. If the event is a generic event, it saves the generic event. Otherwise, it saves the error event.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
