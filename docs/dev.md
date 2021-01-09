Update version number in
* `unicode/__init__.py`
* `package.json`
* in two places in `web/index.html`

Do a github release.


==================
OLD:

# Python Release

```sh
# python checks
pytest
pylint unicodeit

# create package and upload
python setup.py sdist
twine upload dist/unicodeit...
```


# NPM Release

```sh
# update typescript data
python -m unicodeit.export_data

# typescript checks
npm run lint
npm run test

# rebuild typescript bundles
npm run build

# publish
npm publish
```


# Website update

```sh
# follow steps of NPM release first

# push web folder to gh-pages branch
ghp-import --no-jekyll --push web
```
