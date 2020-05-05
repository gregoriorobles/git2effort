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

import logging
import tabulate

from collections import defaultdict, Counter
from datetime import datetime, timezone
from perceval.backends.core.git import Git

from .merging import simplemerge

import sys


def author_counting(authorsdict, period_length, active_days):
    """Given an authordict, and the specified period_length, returns a list with the number commits in each period.
    
    :param authorsdict: dictionary of authors (key: (name, email); value: list of commit dates)
    
    :param period_length: Length of the time period (in months)
    
    :param active_days: Boolean value that determines if we count commits on a same day just once
    
    :returns: list of Counter collections, which counts commits grouped by periods.
    """
    logging.info("Applying effort estimation model.")
    author_counters = []
    commits_same_day = 0
    for author in authorsdict:
        commit_days = []
        dates = []
        for date in authorsdict[author]:
#            print(date.month, int(round((date.month)/12)+1))
            if not active_days or (date.year, date.month, date.day) not in commit_days:
                commit_days.append((date.year, date.month, date.day))
                period = int(round((date.month-1)/(period_length*2))+1)
                dates.append(str(date.year) + "." + str(period))
            else:
                commits_same_day += 1
        author_counters.append(Counter(dates))
    if active_days:
        logging.info("Number of same author commits on the same day: " + str(commits_same_day))
    return author_counters

def project_period_effort(author_counter, threshold, period_length):
    """Given an author counter object (a list of Counters with the commits by periods) and the threshold, returns a dictionary with the total effort (value) for each period (key).
   
    :param author_counter: list of Counter collections, which counts commits grouped by periods.
    
    :param threshold: Threshold value (in commits) to determine if a developers is full-time devoted to the project.
    
    :param period_length: Length of the time period (in months)
    
    :returns: a tuple with:
       a dictionary with the total effort (value) for each period (key)
       a dictionary with the number of full_time developers (value) for each period (key)
       a dictionary with the number of non_full_time developers (value) for each period (key)
    """
    effort_periods = defaultdict(int) 
    full_time_periods = defaultdict(int)
    non_full_time_periods = defaultdict(int)
    for counter in author_counter:
        for period in counter:
            effort = round(counter[period]/threshold * period_length, 2)
            if effort > period_length:   # saturation
                effort = period_length
                full_time_periods[period] += 1
            else:
                non_full_time_periods[period] += 1
#            print(period, counter[period], effort)
            effort_periods[period] += effort
    return (effort_periods, full_time_periods, non_full_time_periods)

def project_period_maxeffort(author_counter, period_length):
    """Given an author counter object (a list of Counters with the commits by periods), returns a dictionary with the maximum possible effort (value) for each period (key).
    
    :param author_counter: list of Counter collections, which counts commits grouped by periods.
    
    :param period_length: Length of the time period (in months)
    
    :returns: dictionary with the maximum possible effort (value) for each period (key).
    """
    effort_periods = defaultdict(int) 
    for counter in author_counter:
        for period in counter:
            effort_periods[period] += period_length
    return effort_periods

def pretty_print_period(period_length, first_commit, headers, *argv):
    """Given a dictionary with values for periods (key), the first commit and the period length, returns a line to be printed. A preprended line with the header (the periods) can be added, if desired.
    
    :param period_length: Length of the time period (in months)

    :param first_commit: datetime object of first commit

    :param headers: TODO

    :param *argv: TODO
            
    :returns: string
    """
    period_lists = []
    for year in range(first_commit.year, datetime.now().year+1):
        for period in range(int(12/period_length)):
            period = str(year) + "." + str(period+1)
            sublist = [period]
            for d in argv:
                sublist += [d[period]]
            period_lists.append(sublist)
    # TODO: remove the previous periods to first commit and the last periods in the future    
    return tabulate.tabulate(period_lists, headers=["Period"] + headers)

def run(args):
    """
    """  
    repo_url = args['git_repository']
    period_length = args['period']
    threshold = args['threshold']
    active_days = True

    # directory for letting Perceval clone the git repo
    # TODO: this is Linux-operating system specific. Should change
    repo_dir = '/tmp/' + repo_url.split('/')[-1] + '.git'

    first_commit = datetime.now(timezone.utc)
    authorDict = defaultdict(list)

    repo = Git(uri=repo_url, gitpath=repo_dir)

    for commit in repo.fetch():
        commitdate = datetime.strptime(commit['data']['AuthorDate'], '%a %b %d %H:%M:%S %Y %z')
        if commitdate < first_commit:
            first_commit = commitdate
        authorDict[commit['data']['Author']].append(commitdate)
    logging.info("Authors found: " + str(len(authorDict)))

    simplemerge(authorDict)
    logging.info("Authors after merge: " + str(len(authorDict)))
    
    author_count = author_counting(authorDict, period_length, active_days)
#    print(author_count)
    (effort_periods, full_time_periods, non_full_time_periods) = project_period_effort(author_count, threshold, period_length)
    maxeffort_periods = project_period_maxeffort(author_count, period_length)

    # Printing results
    print()
    print("CONFIGURATIONS:")
    print("  Length of period (in months):", period_length)
    print("  Threshold t (in commits in a period):", threshold)
    print()
    print("RESULTS:")
    print("  First commit date:", first_commit, "--", round((datetime.now(timezone.utc)-first_commit).days/30, 2) , "months ago")
    print("  Maximum possible development effort (in person-months):", sum(maxeffort_periods.values()))
    print()
    print(pretty_print_period(period_length, first_commit, ["FT", "Non-FT", "Effort"], full_time_periods, non_full_time_periods, effort_periods))
    print(" " * 8, "FT: Full-time developers")
    print()
    print("  ---> Estimated development effort (in person-months):", round(sum(effort_periods.values()), 2))
    print()
    print("For more information, visit http://github.com/gregoriorobles/git2effort")
    print()

