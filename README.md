math-genealogy
=====================

A Python script to generate genealogy graphs for a single or multiple mathematicians, from the [Mathematics Genealogy Project](https://www.genealogy.math.ndsu.nodak.edu), through [Mathematics Genealogy Grapher (Geneagrapher) package](http://www.davidalber.net/geneagrapher/).

## Usage:

```
Usage:
  python build_genealogy.py (--mathid=<id>|--name=<name>)... [--output=<out>]

Options:
  --name=<name>   Name in the form "John Doe" or "John D. Doe"
  --output=<out>  Output file name (.pdf or .png) [default: output.pdf]
```
    
## Installation

	easy_install http://www.davidalber.net/dist/geneagrapher/Geneagrapher-0.2.1-r2.tar.gz
    sudo apt-get install graphviz graphviz-dev
    pip install -r requirements.txt
    
Note that Geneagrapher requires Python 2.

## Examples
### Single person
```
	python build_genealogy.py --mathid=162833
	# or
	python build_genealogy.py --name="Tristan A. Hearn"
```
generates
![Graph](http://i.imgur.com/G9UtDYv.jpg)
### Multiple persons
```
python build_genealogy.py --mathid=162833 --name="Terence Tao" --mathid=110487
```
generates
![Graph](http://i.imgur.com/zelQDx9.jpg)

## TODO
- Methods that will graph just the minimum path between groups individuals, by finding their most recent common grand-advisor
