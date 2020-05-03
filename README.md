# git2effort [![PyPI version](https://badge.fury.io/py/git2effort.svg)](https://badge.fury.io/py/git2effort)

Calculate development effort estimation from a Git repository.

## Usage

```
usage: git2effort [-c <file>] [-g] <git_repository> [<args>] | --help | --version

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version
  -c FILE, --config FILE
                        set configuration file
  -g, --debug           set debug mode on

```

## Requirements

* Python >= 3.4
* perceval >= 0.12
* python3-dateutil >= 2.6
* python3-requests >= 2.7
* python3-bs4 (beautifulsoup4) >= 4.3
* python3-feedparser >= 5.1.3
* python3-dulwich >= 0.18.5
* grimoirelab-toolkit >= 0.1.4

Note that you should have also the following packages installed in your system:
- git
- build-essential

## Installation

There are several ways for installing git2effort on your system: from packages
or from the source code.

### Pip

Perceval can be installed using [pip](https://pip.pypa.io/en/stable/), a tool
for installing Python packages. To do it, run the next command:

```
$ pip3 install git2effort
```

### Source code

To install from the source code you will need to clone the repository first:

```
$ git clone https://github.com/gregoriorobles/git2effort.git
```

Then you can execute the following commands:
```
$ pip3 install -r requirements.txt
$ pip3 install .
```

## References

If you use git2effort in your research papers, please refer to [Estimating development effort in free/open source software projects by mining software repositories: a case study of openstack](https://dl.acm.org/doi/abs/10.1145/2597073.2597107) -- [Pre-print](https://www.researchgate.net/publication/260953482_Estimating_Development_Effort_in_FreeOpen_Source_Software_Projects_by_Mining_Software_Repositories):

### APA style

```
Robles, G., González-Barahona, J. M., Cervigón, C., Capiluppi, A., & Izquierdo-Cortázar, D. (2014, May). Estimating development effort in free/open source software projects by mining software repositories: a case study of openstack. In Proceedings of the 11th Working Conference on Mining Software Repositories (pp. 222-231).
```

### BibTeX

```
@inproceedings{robles2014estimating,
  title={Estimating development effort in free/open source software projects by mining software repositories: a case study of openstack},
  author={Robles, Gregorio and Gonz{\'a}lez-Barahona, Jes{\'u}s M and Cervig{\'o}n, Carlos and Capiluppi, Andrea and Izquierdo-Cort{\'a}zar, Daniel},
  booktitle={Proceedings of the 11th Working Conference on Mining Software Repositories},
  pages={222--231},
  year={2014}
}
```


## Examples

### Perceval

To run this backend execute the next command. Take into account that to run
this backend Git program has to be installed on your system.

```
$ git2effort git 'https://github.com/chaoss/grimoirelab-perceval.git' --from-date '2016-01-01'
```

git2effort can also work with a Git log file as input. We recommend to use the next command to get the most complete log file.

```
git log --raw --numstat --pretty=fuller --decorate=full --parents --reverse --topo-order -M -C -c --remotes=origin --all > /tmp/gitlog.log
```

Then, to run git2effort on it, just execute any of the next commands:

```
$ git2effort --git-log '/tmp/gitlog.log' 'file:///myrepo.git'
```

or

```
$ git2effort '/tmp/gitlog.log'
```


## License

Licensed under GNU General Public License (GPL), version 3 or later.
