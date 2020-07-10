# Release

```sh
# python checks
pytest
pylint unicodeit

# update typescript data
python -m unicodeit.export_data

# typescript checks
npm run lint
npm run test

# rebuild typescript bundles
npm run build
```

Update website:

```sh
ghp-import web --no-jekyll --push gh-pages
```
