# EnteroDocument

Use one Document class across all file formats to extract metadata and text.


## Classes

This module reduces redundant logic by converting some file formats to pdf format, then applying data extraction algorithms to the pdf.  File location can be local, given by `PosixPath`, or the file artifact can be kept in memory (TODO:add automatic streaming processing for large files) after initializing it as `UniformResourceLocator`.

Once the artifact is local, it can processed using `EnteroDocument`, created from `*Factory.build()`.  All `*Factory` classes are configured using the same `EnteroConfig`; although, each uses different aspects of it.


## Installation

There are many dependencies, each with strengths / weaknesses.  EnteroDoc applies the strengths of each; however, this can cause License issues.  Future versions will reduce the number of dependencies and ensure a more flexible license, such as MIT.  Adjust the following configurations in `EnteroConfig`:

```
renderRequestJs = False
applySpacy = False
applyPyMuPdf = False    #TODO
```


### Rendering web content (UniformResourceLocator)

If you want to render the javascript on requested pages using config `renderRequestJs`, then `requests-html` is employed and this feature can be turned-on; however, it requires `pyppeteer`. 

Install `pyppeteer` dependencies by installing chromium, [ref](https://stackoverflow.com/questions/57217924/pyppeteer-errors-browsererror-browser-closed-unexpectedly):

* check dependencies needed with: `ldd ~/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome | grep 'not found'`
* install chromium

```
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update 
sudo apt install google-chrome-stable
```


### Applying models

Spacy is required to process text by using `applySpacy`.

` python -m spacy download en_core_web_sm`


### PDF Processing 

The module `PyMuPdf` is very good at some document extraction logic, such as table of contents, but it has a very restrictive license (AGPL).  If this is appropriate for your use case you can use `applyPyMuPdf` to use this module.



## TODO

* consolidate pdf modules
  - ~~remove pdfkit~~
  - replace pypdf => no, used by xhtml2pdf
  - opt for pdfminer.six (MIT) over pymupdf (AGPL)
* remove or make better use of pandas
* add ocr => OCRmyPDF
* add msft office formats