# D-score

[![DOI](https://zenodo.org/badge/355984069.svg)](https://zenodo.org/badge/latestdoi/355984069)
[![PyPI version](https://badge.fury.io/py/dscore.svg)](https://badge.fury.io/py/dscore)

`dscore` is a meta-server tool for the prediction of disordered regions in protein sequences. It works by querying several webservers and gathering the results in an easy-to-use format. All the work is automated using simple web requests where possible, falling back to webscraping with `selenium` for servers without a public API.

The servers currently used are the following (follow the links for more information and references to papers):
- [disembl](http://dis.embl.de/)
- [disopred](http://bioinf.cs.ucl.ac.uk/psipred/)
- [disprot](http://original.disprot.org/metapredictor.php)
- [espritz](http://old.protein.bio.unipd.it/espritz/)
- [globplot](http://globplot.embl.de/)
- [iupred](https://iupred3.elte.hu/)
- [jpred](https://www.compbio.dundee.ac.uk/jpred/)
- [metapredict](https://metapredict.net)
- [pondr](https://www.pondr.com)
- [prdos](prdos.hgc.jp/cgi-bin/top.cgi)

- [seg](https://mendel.imp.ac.at/METHODS/seg.server.html) (for complexity prediction)

# Features

`dscore` then aggregates the data in a single table in a text file for further processing. It will also automatically generate a few plots for quickly visualising the data.

---
Server summary plot: disorder predictions from each algorithm available and consensus D-score.
![](https://user-images.githubusercontent.com/23482191/205310158-06775023-a62a-4d1c-be4f-df4e7644ebca.png)

---
D-score plot: line plot of the raw averaged value used for D-score prediction.
![](https://user-images.githubusercontent.com/23482191/205310161-29db13e6-5740-46d9-825a-ff15efac553c.png)

---
Consensus plot: an indication of how close to the consensus each server is, useful to find outliers. 
![](https://user-images.githubusercontent.com/23482191/205310156-85074e12-7774-43f5-9f23-169825750794.png)

---
Text outputs: can easily be parsed for more advanced analysis.

```
# 0. resn
# 1. residue
# 2. disprot_VSL2
# 3. disprot_VSL3
# 4. disprot_VLXT
# 5. disprot_PONDR-FIT
# 6. dscore_raw
# 7. dscore
  0  1    2    3    4    5       6  7
---  ---  ---  ---  ---  ---  ----  ---
  1  M    D    D    D    D    0     D
  2  T    D    D    D    D    0     D
  3  K    D    D    D    D    0     D
  4  K    D    D    D    D    0     D
  [...]
```

# Installation

`dscore` is available on PyPi and easily [installable with `pip`](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/):

```
pip install dscore
```

## Firefox webdriver

To run, `dscore` also requires the `Firefox` webdriver to be installed. Download the latest version of the driver [from the official github release](https://github.com/mozilla/geckodriver/releases/latest): scroll down and choose the appropriate one (for example, the `...linux64.tar.gz` for a 64bit linux installation). Make sure to unzip/untar the driver and make it accessible on the `PATH` enviroment variable. [Here's a detailed guide on how to do this](https://dev.to/eugenedorfling/installing-the-firefox-web-driver-on-linux-for-selenium-d45).

# Usage

*Note that this program works by opening a ton of firefox windows and issuing automated commands. Let it do its thing and don't get scared! :)*

**DISCLAIMER**: `dscore` relies on other webservers for its results. Some of these servers have limitations on the amount of requests per user, so you may get temporarily blocked if you submit too many sequences. Spread them out!

`dscore` can be used either as a python library or from the command line. The latter has a simple interface:

```
dscore <sequence_or_fasta_file>
```

Use the `--help` option for more information.

# References

This tool implements a simple automated version of the D-score calculation and analysis performed in the paper [Modular organization of rabies virus phosphoprotein](https://doi.org/10.1016/j.jmb.2009.03.061) by F. Gerard et Al.
