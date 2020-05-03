#!/usr/bin/env python3
#
# Copyright (C) 2020 Gregorio Robles
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Gregorio Robles <grex@gsyc.urjc.es>
#

from collections import defaultdict, Counter
from datetime import datetime, timezone
from perceval.backends.core.git import Git

from .merging import simplemerge

import sys


period_length = 6 # in months. Values can be [1, 2, 3, 4, 6, 12]
threshold = 50 # in number of commits
active_days = True
   
def author_counting(authorsdict):
    author_counters = []
    for author in authorsdict:
        commit_days = []
        dates = []
        for date in authorsdict[author]:
#            print(date.month, int(round((date.month)/12)+1))
            if not active_days or (date.year, date.month, date.day) not in commit_days:
                commit_days.append((date.year, date.month, date.day))
                period = int(round((date.month-1)/(period_length*2))+1)
                dates.append(str(date.year) + "." + str(period))
        author_counters.append(Counter(dates))
    return author_counters

def project_period_effort(author_counter):
    effort_periods = defaultdict(int) 
    for counter in author_counter:
        for period in counter:
            effort = round(counter[period]/threshold * period_length, 2)
            if effort > period_length:   # saturation
                effort = period_length
#            print(period, counter[period], effort)
            effort_periods[period] += effort
    return effort_periods

def project_period_maxeffort(author_counter):
    effort_periods = defaultdict(int) 
    for counter in author_counter:
        for period in counter:
            effort_periods[period] += period_length
    return effort_periods

def project_effort(effort_periods):
    total_effort = 0
    for period in effort_periods:
        total_effort += effort_periods[period]
    return total_effort


def run(repo_url):

    # directory for letting Perceval clone the git repo
    repo_dir = '/tmp/' + repo_url.split('/')[-1] + '.git'

    first_commit = datetime.now(timezone.utc)
    authorDict = defaultdict(list)

    # create a Git object, pointing to repo_url, using repo_dir for cloning
    repo = Git(uri=repo_url, gitpath=repo_dir)
    # fetch all commits as an iterator, and iterate it
    for commit in repo.fetch():
        commitdate = datetime.strptime(commit['data']['AuthorDate'], '%a %b %d %H:%M:%S %Y %z')
        if commitdate < first_commit:
            first_commit = commitdate
        authorDict[commit['data']['Author']].append(commitdate)

    print("First commit:", first_commit)
    print(authorDict.keys())
    print(simplemerge(authorDict))
    print(authorDict.keys())
    author_count = author_counting(authorDict)
    print(author_count)
    effort_periods = project_period_effort(author_count)
    maxeffort_periods = project_period_maxeffort(author_count)
    print(effort_periods)
    print(round(project_effort(effort_periods), 2))
    print(project_effort(maxeffort_periods))
