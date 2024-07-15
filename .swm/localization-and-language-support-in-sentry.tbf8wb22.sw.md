---
title: Localization and Language Support in Sentry
---
This document will cover the process of managing localization files and extending language support in the Sentry application. We'll cover:

1. How localization files are managed in the application.
2. The process of extending language support.
3. How to add a new language to the application.

<SwmSnippet path="/webpack.config.ts" line="126">

---

# Managing Localization Files

Localization files are managed in the `webpack.config.ts` file. The `localeCatalogPath` constant points to the location of the localization catalog, which is a JSON file containing supported locales. The `localeCatalog` constant reads this file and parses it into a `LocaleCatalog` object, which includes an array of supported locales.

```typescript

// Locale compilation and optimizations.
//
// Locales are code-split from the app and vendor chunk into separate chunks
// that will be loaded by layout.html depending on the users configured locale.
//
// Code splitting happens using the splitChunks plugin, configured under the
// `optimization` key of the webpack module. We create chunk (cache) groups for
// each of our supported locales and extract the PO files and moment.js locale
// files into each chunk.
//
// A plugin is used to remove the locale chunks from the app entry's chunk
// dependency list, so that our compiled bundle does not expect that *all*
// locale chunks must be loaded
const localeCatalogPath = path.join(
  __dirname,
  'src',
  'sentry',
  'locale',
  'catalogs.json'
);
```

---

</SwmSnippet>

<SwmSnippet path="/webpack.config.ts" line="156">

---

# Extending Language Support

To extend language support, a new locale needs to be added to the `localeCatalog` object. The `localeToLanguage` function is used to translate a locale name to a language code. The `supportedLocales` constant is an array of all supported locales, and `supportedLanguages` is an array of all supported languages, derived from `supportedLocales`.

```typescript
// Translates a locale name to a language code.
//
// * po files are kept in a directory represented by the locale name [0]
// * moment.js locales are stored as language code files
//
// [0] https://docs.djangoproject.com/en/2.1/topics/i18n/#term-locale-name
const localeToLanguage = (locale: string) => locale.toLowerCase().replace('_', '-');
const supportedLocales = localeCatalog.supported_locales;
const supportedLanguages = supportedLocales.map(localeToLanguage);
```

---

</SwmSnippet>

<SwmSnippet path="/bin/find-good-catalogs" line="26">

---

# Adding a New Language

To add a new language, the `supported_locales` array in the `catalog_file` needs to be updated. This file is read, the new locale is added to the `supported_locales` array, and the file is then written back with the updated array.

```
    with open(catalog_file) as f:
        rv = json.load(f)["supported_locales"]

    base = "src/sentry/locale"
    for locale in os.listdir(base):
        fn = os.path.join(base, locale, "LC_MESSAGES", "django.po")
        if not os.path.isfile(fn):
            continue

        total_count = 0
        translated_count = 0
        with open(fn) as f:
            catalog = read_po(f)
            for msg in catalog:
                total_count += 1
                if is_translated(msg):
                    translated_count += 1
        pct = translated_count / float(total_count) * 100
        click.echo("% -7s % 2d%%" % (locale, pct), err=True)
        if pct >= MINIMUM and locale not in rv:
            rv.append(locale)
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="follow-up"><sup>Powered by [Swimm](/)</sup></SwmMeta>
