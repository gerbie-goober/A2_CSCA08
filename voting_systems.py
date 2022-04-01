"""CSC108/A08: Fall 2021 -- Assignment 2: voting

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Sophia Huynh, Sadia Sharmin,
Elizabeth Patitsas, Anya Tafliovich.

"""

from typing import List

from constants import (COL_RIDING, COL_VOTER, COL_RANK, COL_RANGE,
                       COL_APPROVAL, APPROVAL_TRUE, APPROVAL_FALSE,
                       SEPARATOR)

# In the following docstrings, 'VoteData' refers to a list of 5
# elements of the following types:
#
# at index COL_RIDING: int         (this is the riding number)
# at index COL_VOTER: int         (this is the voter number)
# at index COL_RANK: List[str]   (this is the rank ballot)
# at index COL_RANGE: List[int]   (this is the range ballot)
# at index COL_APPROVAL: List[bool]  (this is the approval ballot)

###############################################################################
# Task 0: Creating example data
###############################################################################

SAMPLE_DATA_1 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
                  [False, True, False, False]],
                 [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
                  [False, False, True, True]],
                 [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
                  [False, True, False, True]],
                 [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
                  [True, False, True, True]]]
SAMPLE_ORDER_1 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']


SAMPLE_DATA_2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [5, 4, 0, 0],
                  [True, True, False, False]],
                 [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [5, 5, 5, 4],
                  [True, True, True, True]],
                 [72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [5, 1, 1, 0],
                  [True, True, True, False]]]
SAMPLE_ORDER_2 = ['GREEN', 'LIBERAL', 'CPC', 'NDP']

SAMPLE_DATA_3 = [[117, 12, ['a'], [5], [True]],
                 [117, 21, ['a'], [5], [True]],
                 [0, 1, ['a'], [5], [False]],]
SAMPLE_ORDER_3 = ['a']



###############################################################################
# Task 1: Data cleaning
###############################################################################

def clean_data(data: List[List[str]]) -> None:
    """Modify data so that the applicable string values are converted to
    their appropriate type, making data of type List['VoteType'].

    Pre: Each item in data is in the format
     at index COL_RIDING: a str that can be converted to an integer (riding)
     at index COL_VOTER: a str that can be converted to an integer (voter ID)
     at index COL_RANK: a SEPARATOR-separated non-empty string (rank ballot)
     at index COL_RANGE: a SEPARATOR-separated non-empty string of ints
                         (range ballot)
     at index COL_APPROVAL: a SEPARATOR-separated non-empty string of
                         APPROVAL_TRUE's and APPROVAL_FALSE's (approval ballot)

    >>> data = [['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]
    >>> expected = [[0, 1, ['NDP', 'Liberal', 'Green', 'CPC'], [1, 4, 2, 3],
    ... [False, True, False, False]]]
    >>> clean_data(data)
    >>> data == expected
    True
    >>> data = [['112', '100', 'a;abc;cc', '1;4;2', 'YES;YES;YES']]
    >>> expected = [[112, 100, ['a', 'abc', 'cc'], [1, 4, 2],
    ... [True, True, True]]]
    >>> clean_data(data)
    >>> data == expected
    True
    """
    for row in data:
        #modify the riding number
        row[COL_RIDING] = int(row[COL_RIDING])
        #modify the voter number
        row[COL_VOTER] = int(row[COL_VOTER])
        #modify the list of parties
        row[COL_RANK] = row[COL_RANK].rsplit(SEPARATOR)
        #modify the list of range ballots
        range_list = []
        for j in row[COL_RANGE].rsplit(SEPARATOR):
            range_list.append(int(j))
        row[COL_RANGE] = range_list
        #modify the list of approval ballots
        approval_list = []
        split_list = row[COL_APPROVAL].rsplit(SEPARATOR)
        for j in split_list:
            approval_list.append(j == APPROVAL_TRUE)
        row[COL_APPROVAL] = approval_list

###############################################################################
# Task 2: Data extraction
###############################################################################

def extract_column(data: List[list], column: int) -> list:
    """Return a list containing only the elements at index column for each
    sublist in data.

    Pre: each sublist of data has an item at index column.

    >>> extract_column([[1, 2, 3], [4, 5, 6]], 2)
    [3, 6]
    >>> extract_column([[1], [4]], 0)
    [1, 4]
    """
    extract_list = []
    for row in data:
        extract_list.append(row[column])
    return extract_list


def extract_single_ballots(data: List['VoteData']) -> List[str]:
    """Return a list containing only the highest ranked candidate from
    each rank ballot in voting data data.

    Pre: data is a list of valid 'VoteData's
         The rank ballot is at index COL_RANK for each voter.

    >>> extract_single_ballots(SAMPLE_DATA_1)
    ['NDP', 'LIBERAL', 'GREEN', 'LIBERAL']
    >>> extract_single_ballots(SAMPLE_DATA_2)
    ['LIBERAL', 'GREEN', 'NDP']
    >>> extract_single_ballots(SAMPLE_DATA_3)
    ['a', 'a', 'a']
    """
    extract_single_list = []
    for row in data:
        extract_single_list.append(row[COL_RANK][0])
    return extract_single_list


def get_votes_in_riding(data: List['VoteData'],
                        riding: int) -> List['VoteData']:
    """Return a list containing only voting data for riding riding from
    voting data data.

    Pre: data is a list of valid 'VoteData's

    >>> expected = [[1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
    ...              [False, False, True, True]],
    ...             [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
    ...              [False, True, False, True]],
    ...             [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
    ...              [True, False, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_1, 1) == expected
    True
    >>> expected = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [5, 4, 0, 0],
    ... [True, True, False, False]],
    ... [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [5, 5, 5, 4],
    ... [True, True, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_2, 117) == expected
    True
    """

    riding_votes_list = []
    for row in data:
        if row[COL_RIDING] == riding:
            riding_votes_list.append(row)
    return riding_votes_list


###############################################################################
# Task 3.1: Plurality Voting System
###############################################################################

def voting_plurality(single_ballots: List[str],
                     party_order: List[str]) -> List[int]:
    """Return the total number of ballots cast for each party in
    single-candidate ballots single_ballots, in the order specified in
    party_order.

    Pre: each item in single_ballots appears in party_order

    >>> expected = [1, 3, 0, 1]
    >>> expected == voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_1)
    True
    >>> expected = [3, 0, 1, 1]
    >>> expected == voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_2)
    True
    """
    num_ballots = []
    for party in party_order:
        num_ballots.append(single_ballots.count(party))
    return num_ballots


###############################################################################
# Task 3.2: Approval Voting System
###############################################################################

# Note: even though the only thing we need from party_order in this
# function is its length, we still design all voting functions to
# receive party_order, for consistency and readability.
def voting_approval(approval_ballots: List[List[bool]],
                    party_order: List[str]) -> List[int]:
    """Return the total number of approvals for each party in approval
    ballots approval_ballots, in the order specified in party_order.

    Pre: len of each sublist of approval_ballots is len(party_order)
         the approvals in each ballot are specified in the order of party_order

    >>> voting_approval([[True, True, False, False],
    ...                  [False, False, False, True],
    ...                  [False, True, False, False]], SAMPLE_ORDER_1)
    [1, 2, 0, 1]
    >>> voting_approval([[False, True, False, False],
    ...                  [False, True, False, False],
    ...                  [False, True, False, False]], SAMPLE_ORDER_2)
    [0, 3, 0, 0]
    """
    vote_appr_list = []
    j = 0
    while j < len(party_order):
        counter = 0
        for row in approval_ballots:
            if row[j]:
                counter += 1
        vote_appr_list.append(counter)
        j += 1
    return vote_appr_list

###############################################################################
# Task 3.3: Range Voting System
###############################################################################

def voting_range(range_ballots: List[List[int]],
                 party_order: List[str]) -> List[int]:
    """Return the total score for each party in range ballots
    range_ballots, in the order specified in party_order.

    Pre: len of each sublist of range_ballots is len(party_order)
         the scores in each ballot are specified in the order of party_order

    >>> voting_range([[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]],
    ...              SAMPLE_ORDER_1)
    [7, 12, 6, 8]
    >>> voting_range([[0, 1, 1, 10], [0, 0, 0, 10], [0, 1, 1, 10]],
    ...              SAMPLE_ORDER_2)
    [0, 2, 2, 30]
    """
    total_score = []
    j = 0
    while j < len(party_order):
        total_sum = 0
        for row in range_ballots:
            total_sum += row[j]
        total_score.append(total_sum)
        j += 1
    return total_score


###############################################################################
# Task 3.4: Borda Count Voting System
###############################################################################

def voting_borda(rank_ballots: List[List[str]],
                 party_order: List[str]) -> List[int]:
    """Return the Borda count for each party in rank ballots rank_ballots,
    in the order specified in party_order.

    Pre: each ballot contains all and only elements of party_order

    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_1)
    [4, 4, 8, 2]
    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_2)
    [4, 8, 4, 2]
    """
    borda_list = []
    for party in party_order:
        count = 0
        for j in rank_ballots:
            count += (len(party_order) - j.index(party) - 1)
        borda_list.append(count)
    return borda_list


###############################################################################
# Task 3.5: Instant Run-off Voting System
###############################################################################

def remove_party(rank_ballots: List[List[str]], party_to_remove: str) -> None:
    """Change rank ballots rank_ballots by removing the party
    party_to_remove from each ballot.

    Pre: party_to_remove is in all of the ballots in rank_ballots.

    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'GREEN', 'CPC'],
    ...             ['CPC', 'LIBERAL', 'GREEN'],
    ...             ['CPC', 'GREEN', 'LIBERAL']]
    True
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'GREEN')
    >>> ballots == [['LIBERAL','CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL'],
    ...            ['NDP', 'CPC','LIBERAL']]
    True
    """
    for row in rank_ballots:
        row.remove(party_to_remove)


def get_lowest(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the lowest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_lowest([16, 100, 4, 200], SAMPLE_ORDER_1)
    'LIBERAL'
    >>> get_lowest([1, 1, 1, 1], SAMPLE_ORDER_2)
    'GREEN'
    """
    index = party_tallies.index(min(party_tallies))
    return party_order[index]


def get_winner(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the highest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_winner([16, 100, 4, 200], SAMPLE_ORDER_1)
    'NDP'
    >>> get_winner([1, 1, 1, 1], SAMPLE_ORDER_2)
    'GREEN'
    """
    index = party_tallies.index(max(party_tallies))
    return party_order[index]


def voting_irv(rank_ballots: List[List[str]], party_order: List[str]) -> str:
    """Return the party which wins when IRV is performed on the list of
    rank ballots rank_ballots. Change rank_ballots and party_order as
    needed in IRV, removing parties that are eliminated in the
    process. Each ballot in rank_ballots is ordered by party_order.

    Pre: each ballot contains all and only elements of party_order
         len(rank_ballots) > 0

    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> voting_irv(ballots, order)
    'NDP'
    >>> ballots == [['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL']]
    True
    >>> order
    ['LIBERAL', 'NDP']

    >>> order = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> ballots = [['b', 'c', 'd', 'a', 'e', 'f'],
    ...            ['f', 'b', 'c', 'd', 'e', 'a'],
    ...            ['a', 'b', 'c', 'e', 'd', 'f'],
    ...            ['b', 'c', 'a', 'e', 'd', 'f'],
    ...            ['a', 'b', 'c', 'e', 'd', 'f'],
    ...            ['a', 'b', 'c', 'e', 'd', 'f']]
    >>> voting_irv(ballots, order)
    'b'
    >>> ballots == [['b'],
    ...            ['b'],
    ...            ['b'],
    ...            ['b'],
    ...            ['b'],
    ...            ['b']]
    True
    >>> order
    ['b']

    >>> order = ['a', 'b']
    >>> ballots = [['b', 'a'],
    ...             ['a', 'b'],
    ...             ['b', 'a'],
    ...             ['a', 'b'],
    ...             ['a', 'b']]
    >>> voting_irv(ballots, order)
    'a'
    >>> ballots == [['b', 'a'],
    ...             ['a', 'b'],
    ...             ['b', 'a'],
    ...             ['a', 'b'],
    ...             ['a', 'b']]
    True
    >>> order
    ['a', 'b']

    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL'],
    ...            ['LIBERAL', 'CPC', 'NDP', 'GREEN'],
    ...            ['LIBERAL', 'GREEN', 'NDP', 'CPC'],
    ...            ['GREEN', 'NDP', 'LIBERAL', 'CPC'],
    ...            ['NDP', 'LIBERAL', 'CPC', 'GREEN'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['GREEN', 'NDP', 'CPC', 'LIBERAL']]
    >>> voting_irv(ballots, order)
    'NDP'
    >>> ballots == [['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['LIBERAL', 'NDP'],
    ...             ['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL']]
    True
    >>> order
    ['LIBERAL', 'NDP']

    >>> ballots = [['a'], ['a'], ['a']]
    >>> order = ['a']
    >>> voting_irv(ballots, order)
    'a'
    >>> order
    ['a']
    """
    votes_to_win = int(len(rank_ballots) // 2) + 1
    votes = 0
    while votes <= votes_to_win:
        #list that stores the number of times each party is first
        party_to_firsts = []
        #add parties to firsts_list
        firsts_list = extract_column(rank_ballots, 0)
        #add number of firsts for each party to party_to_firsts
        for party in party_order:
            party_to_firsts.append(firsts_list.count(party))
        #return once there is a party with votes_to_win or more
        #or last two parties are tied and must choose the second one.
        if max(party_to_firsts) >= votes_to_win or len(party_order) == 1:
            return get_winner(party_to_firsts, party_order)
        #only eliminates losers in remove_party and rank_ballots
        #until down to two parties or one party if tied
        loser = get_lowest(party_to_firsts, party_order)
        party_to_firsts.pop(party_order.index(loser))
        party_order.remove(loser)
        remove_party(rank_ballots, loser)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
