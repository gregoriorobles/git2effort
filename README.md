# git2effort [![PyPI version](https://badge.fury.io/py/git2effort.svg)](https://badge.fury.io/py/git2effort)

Calculate development effort estimation from a Git repository.

## Usage

```
usage: git2effort [-g] [<args>] <git_repository> | --help | --version

optional arguments:
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold value (in commits) to determine if a
                        developers is full-time devoted to the project.
                        Default=75.
  -p PERIOD, --period PERIOD
                        Length of the time period (in months). Default=6.

optional arguments:
  -g, --debug           set debug mode on
  -h, --help            show this help message and exit
  -v, --version         show version

```

## Requirements

* Python >= 3.4
* perceval >= 0.12
* python3-dateutil >= 2.6
* python3-requests >= 2.7
* python3-bs4 (beautifulsoup4) >= 4.3
* python3-feedparser >= 5.1.3
* python3-dulwich >= 0.18.5
* tabulate >= 0.8.7
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


## Understanding git2effort

The threshold t determines what developers are considered full-time in a period
of time p. So, if in p months a developer does t commits, the developer is
full-time. If not, his/her contributions will be a fraction of that.

The value of the threshold t depends on the project, in particular, on its
process (e.g., if there is a review process in place, if there is commit
squashing when merging). Below you can find a list of projects that can serve
as an example. The t values given below are supported by feedback provided
by the developers of these projects.

```
Example threshold t values (for a default period of 6 months):
    12: Strong review process with commit squashing, like in OpenStack and Moodle
    18: Review process with commit squashing, like in Linux and Webkit
    30: Soft review process, like in Mediawiki
    50: Strong pull-request-driven process, like in Ceph
    75: Soft pull-request-driven process, like in git2effort
   100: Non-engineered process
```

### Example: Running git2effort on Perceval

To estimate the effort for a Git repository, execute the next command. Take into
account that Git has to be installed on your system.

In the case of Perceval, we assume that it is a project that follows a strong
pull-request-driven process, like the one in Ceph, so we choose a threshold
value of 50:

```
$ git2effort --threshold=50 https://github.com/chaoss/grimoirelab-perceval.git
```

### Example: Running git2effort on git2effort

To estimate the effort for a Git repository, execute the next command. Take into
account that Git has to be installed on your system.

In the case of git2effort, we assume that it is a project that follows a soft
pull-request-driven process, so we choose a threshold value of 75 (as this is 
the default one in git2effort we do not need to specify it):

```
$ git2effort https://github.com/gregoriorobles/git2effort
```

## Research in Progress

This is research in progress. If you have any comments or suggestions, please contact me (grex at gsyc.urjc.es). I will be more than happy to hear to your feedback.


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


## License

Licensed under GNU General Public License (GPL), version 3 or later.
