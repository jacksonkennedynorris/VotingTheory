# Jackson Norris
# CSC 375: Voting Theory 
# Project 1
# IMPLEMENTING SINGLE VOTER

import random
import csv
from itertools import combinations 

# A Voter has a name, and a ballot. I also included a top_choice method to quickly implement plurality. 
class Voter: 
    def __init__(self,voter_id,n): 
        self.name = chr(ord('`')+voter_id)
        self.alternative_options = list(range(1,n+1))
        self.preferences = self.cast_ballot(n)
        self.n = len(self.alternative_options)
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

def is_first_preferred(i,j, ballot): 
    first_index = ballot.index(i)
    second_index = ballot.index(j)
    if first_index < second_index: 
        return 1
    return 0


# This function takes the electorate and returns the condorcet winner. If there is no condorcet winner, the function returns 0 (which evalutes to false in Python). 
def condorcet_winner(electorate): 
    n = electorate[0].n
    condorcet = []
    for i in range(n): 
        condorcet.append(0)
    for combo in combinations(range(1,n+1),2):
        first,second = 0,0
        for ballot in electorate: 
            if is_first_preferred(combo[0],combo[1],ballot.preferences):
                first = first + 1
            else:
                second = second + 1
        if first > second: 
            condorcet[combo[0]-1] = condorcet[combo[0]-1] + 1
        else: 
            condorcet[combo[1]-1] = condorcet[combo[1]-1] + 1
    for candidate in condorcet: 
        if candidate == len(condorcet) - 1: 
            return condorcet.index(candidate) + 1
    return 0 


def borda_winner(electorate): 
    borda = []
    for i in range(1,electorate[0].n+1): 
        borda.append(0)
    for voter in electorate: 
        points = len(voter.preferences) - 1 
        for alt in voter.preferences: 
            borda[alt - 1] = borda[alt - 1] + points
            points = points - 1
    return borda.index(max(borda)) + 1

def plurality_winner(electorate): 

    candidates = electorate[0].alternative_options
    plurality = []  
    for i in candidates: 
        plurality.append(0)
    for voter in electorate: 
        plurality[voter.top_choice() - 1] = plurality[voter.top_choice() - 1] + 1
    max_votes = max(plurality) 
    count = 0
    for element in plurality: 
        if element == max_votes: 
            if count == 1: 
                return 0 
            else: 
                count = count + 1
    return plurality.index(max_votes) + 1

def copeland_winner(electorate): 
    candidates = electorate[0].alternative_options
    copeland = []
    for i in candidates: 
        copeland.append(0)
    for combo in combinations(candidates,2):
        first,second = 0,0
        for ballot in electorate: 
            if is_first_preferred(combo[0],combo[1],ballot.preferences): 
                first = first + 1
            else: 
                second = second + 1
        if first < second: 
            copeland[combo[0] - 1] = copeland[combo[0] - 1] - 1
            copeland[combo[1] - 1] = copeland[combo[1] - 1] + 1
        else: 
            copeland[combo[0] - 1] = copeland[combo[0] - 1] + 1
            copeland[combo[1] - 1] = copeland[combo[1] - 1] - 1
    max_cope = max(copeland)
    time = 0
    for element in copeland:
        if element == max_cope: 
            if time == 1: 
                return 0 
            time = time + 1
    return copeland.index(max(copeland)) + 1

def main(): 
    m_list = [] 
    n_list = []
    with open('data','w',newline = '') as csvfile: 
        fieldnames = ["voters","alternatives","condorcet","borda_picks_condorcet","plurality_picks_condorcet","all_agree","borda_and_copeland","borda_and_plurality","copeland_and_plurality"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  
    for i in range(1,8):
        m_list.append(2**i)
        n_list.append(2**i + 1)
    for m in m_list: 
        for n in n_list: 
            con_count,plu_count,bor_count,cope_count,bor_plu,bor_cope,plu_cope,all_three = 0,0,0,0,0,0,0,0
            for i in range(10000): 

                electorate = []

                for voter_id in range(1,n + 1): 
                    voter = Voter(voter_id,m)
                    electorate.append(voter)

                condorcet = condorcet_winner(electorate)
                plurality = plurality_winner(electorate)
                borda = borda_winner(electorate)
                copeland = copeland_winner(electorate)

                if condorcet: 
                    if plurality == condorcet: 
                        plu_count = plu_count + 1
                    if borda == condorcet: 
                        bor_count = bor_count + 1
                    if copeland == condorcet: 
                        cope_count = cope_count + 1
                    con_count = con_count + 1
                    assert copeland == condorcet, "Condorcet winner exists. Thus Copeland should be " + str(condorcet) + ", not " + str(copeland)
                ## Case there is no condorcet winner 
                else: 
                    if borda == plurality and borda == copeland and copeland == plurality: 
                        all_three = all_three + 1
                    if borda == plurality:
                        bor_plu = bor_plu + 1
                    if borda == copeland: 
                        bor_cope = bor_cope + 1
                    if plurality == copeland: 
                        plu_cope = plu_cope + 1 
            not_condorcet = 10000 - con_count
            print("")
            print("")
            print("")
            print("")
            print("Number of voters: ", n)
            print("Number of alternatives: ", m)
            print("")
            con_percent = con_count/100
            print("Condorcet: ",con_percent,"%")
            bor_percent = 100*(bor_count/con_count)
            print("Borda picks Condorcet winner: ", bor_percent,"%"," of the time.")
            plu_percent = 100*(plu_count/con_count)
            print("Plurality picks Condorcet winner: ", plu_percent,"%"," of the time.")
            print("")
            all_three_percent,bor_plu_percent,bor_cope_percent,plu_cope_percent = -1,-1,-1,-1
            if not_condorcet: 
                print("When condorcet doesn't exist... ")
                all_three_percent = 100*(all_three/not_condorcet)
                print("Borda, Plurality, and Copeland all agree ", all_three_percent,"%","of the time.")
                bor_plu_percent = 100*(bor_plu/not_condorcet)
                print("Borda and Plurality agree ",bor_plu_percent,"%"," of the time.")
                bor_cope_percent = 100*(bor_cope/not_condorcet)
                print("Borda and Copeland agree ",bor_cope_percent, "%","of the time.")
                plu_cope_percent = 100*(plu_cope/not_condorcet)
                print("Plurality and Copeland agree ", plu_cope_percent,"%","of the time.")
            with open("data", 'a', newline= '') as csvfile: 
                writer = csv.writer(csvfile) 
                row = [n,m,con_percent,bor_percent,plu_percent,all_three_percent,bor_plu_percent,bor_cope_percent,plu_cope_percent]
                writer.writerow(row)

main()