# D-score

`dscore` is a meta-server tool for the prediction of disordered regions in protein sequences. It works by querying several webservers and gathering the results in an easy-to-use format. All the work is automated using simple web requests where possible, falling back to webscraping with `selenium` for servers without a public API.

# Installation

`dscore` is available on PyPi and easily installable with `pip`:

```
pip install dscore
```

## Firefox webdriver

To run, `dscore` also requires the `Firefox` webdriver to be installed. Download the latest version of the driver [from the official github release](https://github.com/mozilla/geckodriver/releases/latest): scroll down and choose the appropriate one (for example, the `...linux64.tar.gz` for a 64bit linux installation). Make sure to unzip/untar the driver and make it accessible on the `PATH` enviroment variable. [Here's a detailed guide on how to do this](https://dev.to/eugenedorfling/installing-the-firefox-web-driver-on-linux-for-selenium-d45).


# Usage

*Note that this program works by opening a ton of firefox windows and issuing automated commands. Let it do its thing and don't get scared! :)*

`dscore` can be used either as a python library or from the command line. The latter has a simple interface:

```
dscore --help
```

For example, to save results as a csv and make a plot, using a fasta file as input, run:

```
dscore -cp my_proteins.fasta -o output_dir
```

You will find the output files inside `output_dir`, including raw data in csv format and plots.
