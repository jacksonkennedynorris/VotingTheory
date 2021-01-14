# Jackson Norris
# CSC 375: Voting Theory 
# Project 1
# IMPLEMENTING SINGLE VOTER

import random

class Voter: 
    def __init__(self,voter_id,n): 
        self.name = chr(ord('`')+voter_id)
        self.preferences = self.cast_ballot(n)
        self.n = len(self.preferences)
    def cast_ballot(self, n):
        ballot = []
        while len(ballot) < n:
            rand = random.randint(1,n)
            if rand not in ballot: 
                ballot.append(rand) 
        assert max(ballot) == len(ballot)
        return ballot 
    def top_choice(self): 
        return self.preferences[0]

def condorcet_winner(electorate): 
    n = electorate[0].n
    for first in range(1,n+1): 
        flag = True 
        for second in range(1,n+1): 
            if first == second: 
                continue 
            count = 0
            for ballot in electorate: 
                first_index = ballot.preferences.index(first)
                second_index = ballot.preferences.index(second)
                if first_index < second_index: 
                    count = count + 1
            if count < len(electorate)/2:
                flag = False
        if flag: 
            return first 
    return 0

def borda_winner(electorate): 
    borda = []
    for i in range(1,electorate[0].n+1): 
        borda.append(0)
    for voter in electorate: 
        i = 1
        for preference in voter.preferences: 
            borda[preference - 1] += len(voter.preferences) - i 
            i = i + 1
    print(borda)
    return 

def main(): 

    for m in range(3,26): 
        for n in range(1,26): 
            condorcet = 0
            for i in range(10000): 

                electorate = []

                for i in range(1,n + 1): 
                    voter = Voter(i,m)
                    electorate.append(voter)
                c_win = condorcet_winner(electorate)
                b_win = borda_winner(electorate)
                if c_win:
                    condorcet = condorcet + 1
                else: 
                    pass 
            #print(condorcet/100,"%")
                

main()