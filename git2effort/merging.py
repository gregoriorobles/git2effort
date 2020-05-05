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


def same(authors):
    """Given a list of author (name, email) duples, returns a list with those having the same name ore same e-mail.

    :param authors: list of authors (name, email)
    For instance: [("John Smith", "jsmith@gmail.com"), ("John Smith", a@b.com")]

    :returns: a list of lists with authors having the same name or the same email
    In the previous example, returns [("John Smith", "jsmith@gmail.com"), ("John Smith", a@b.com")]
        """
    return_list = []
    tmp_list = [] # This list will contain triples of author, name and email
    name_set = set()
    email_set = set()
    for author in authors:
        name, email = author.split('<')
        email.replace('>', '')
        # FIXME: This requires refactoring, as we have the same algorithm twice
        if name in name_set:
            for other_author, other_name, _ in tmp_list:
                if other_name == name:
                    return_list.append([other_author, author])
                    logging.debug("Authors merged: " + str(other_author) + " " + str(author))
        else:
            name_set.add(name)
        if email in email_set:
            for other_author, _, other_email in tmp_list:
                if other_email == email:
                    return_list.append([other_author, author])
                    logging.debug("Authors merged: " + str(other_author) + " " + str(author))
        else:
            email_set.add(email)
        tmp_list.append([author, name, email])
    return return_list

def simplemerge(authorsdict):
    """Given an authordict
           key is the (name, email) tuple
           value is a list with all commit dates
    Returns an authordict but with authors with the same name or the same email merged.

    :param authorsdict: dictionary of authors (key: (name, email); value: list of commit dates)

    :returns: dictionary of authors (key: (name, email); value: list of commit dates); merged when name or email of other authors are the same
        """
    logging.info("Looking for authors to merge.")
    same_authors = same(authorsdict.keys())
    for match1, match2 in same_authors:
        authorsdict[match1] = authorsdict[match1] + authorsdict[match2]
        del(authorsdict[match2])
    return authorsdict
