# UnicodeIt

Converts latex tags into unicode. Available online at www.unicodeit.net or as Automator script for the Mac.

* Online Version: www.unicodeit.net for any platform
* Linux wrapper: http://code.google.com/p/unicodeitlinux/
* Introductory Slides: http://www.svenkreiss.com/wiki/images/5/5e/UnicodeItSlides.pdf



# Development Notes

### Creating Automator Release

```
cd src
python convert.py
```

* Open unicodeit.py with some editor and copy it's content.
* Open Automator and the workflow that sits in the computers `Services` directory.
* Paste.
* `Export...` the workflow into the Automator directory.
* Open the directory in Finder.
* Select `LICENSE` and the workflow file: `Compress`, rename, move to `versions` folder in gh-pages branch.
* Update link on `unicodeit.net`.

Repeat for `clipboard` version.


### Updating unicodeit.net

```
cd src
python convert.py
```

* `cp unicodeit.js ../../UnicodeitGhPages/`

