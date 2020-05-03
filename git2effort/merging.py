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

def same(authors):
    return_list = []
    tmp_list = [] # This list will contain triples of author, name and email
    name_set = set()
    email_set = set()
    for author in authors:
        name, email = author.split('<')
        email.replace('>', '')
        if name in name_set:
            for other_author, other_name, _ in tmp_list:
                if other_name == name:
                    return_list.append([other_author, author])
        else:
            name_set.add(name)
        if email in email_set:
            for other_author, _, other_email in tmp_list:
                if other_email == email:
                    return_list.append([other_author, author])
        else:
            email_set.add(email)
        tmp_list.append([author, name, email])
    return return_list

def simplemerge(authorsdict):
    same_authors = same(authorsdict.keys())
    for match1, match2 in same_authors:
        authorsdict[match1] = authorsdict[match1] + authorsdict[match2]
        del(authorsdict[match2])
    return authorsdict
