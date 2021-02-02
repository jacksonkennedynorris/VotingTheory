# project3.py
# I would like you to:
# 1. Adapt this code to implement k-Approval.
# 2. Implement the Greedy Approximation to Chamberlin-Courant rule.
# 3. Run about 10 simulations each of these three, to get 
#       a feel for what they output.
# 4. For each of the three rules, run new simulations until you 
#       get an image that you believe is representative.
# 5. Save the images you selected, and caption them. 
#   Describe your findings, and comment on whether the results 
#   match the claimed goals of the rules. 

import numpy as np
import matplotlib.pyplot as plt

def euclid2d(x1, y1, x2, y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def get_2d_gaussian_points(N):
    x = np.random.normal(loc=0.0, scale=1.0, size=N)
    y = np.random.normal(loc=0.0, scale=1.0, size=N)
    return x, y

def get_2d_gaussian_mixture_points(N):
    offset = 1.0
    stdev = 0.7

    x1 = np.random.normal(loc=-1*offset, scale=stdev, size=int(np.ceil(N/2)))
    y1 = np.random.normal(loc=-1*offset, scale=stdev, size=int(np.ceil(N/2)))

    x2 = np.random.normal(loc=offset, scale=stdev, size=int(np.floor(N/2)))
    y2 = np.random.normal(loc=offset, scale=stdev, size=int(np.floor(N/2)))

    x1.shape = (-1, 1)
    x2.shape = (-1, 1)

    y1.shape = (-1, 1)
    y2.shape = (-1, 1)

    x = np.vstack((x1, x2))
    y = np.vstack((y1, y2))

    return x, y

def get_cand_scores(x_cand,y_cand,x_vote,y_vote,k,system,candidates):
    # This function is adapted from the previous borda function. I wanted a function that would spit out the 
    # candidate scores rather than their x and y.
    # "System" is a string of borda, cc, or k-approval. 
    # Committee is used exclusively for calculating chamberlin-courant. 

    cand_scores = np.zeros_like(x_cand)
    og_indicies = np.arange(0, len(x_cand))
    og_indicies.shape = (-1,1)

    for i in range(len(x_vote)):
        distances = np.zeros_like(x_cand)
        distances.shape = (-1,1)
        for j in range(len(x_cand)):
            # Compute distances
            distances[j] = euclid2d(x_vote[i], y_vote[i], x_cand[j], y_cand[j])
            sortable = np.hstack((og_indicies, distances))

        # Sort into preference order
        sortable = sortable[sortable[:,1].argsort()]
        
        if system == "borda": 
            # Assign points
            for l in range(len(cand_scores)):
                cand_scores[int(sortable[l,0])] += len(cand_scores) - l - 1
        elif system == "k-approval": 
            for num in range(k):
                cand_scores[int(sortable[num][0])] = cand_scores[int(sortable[num][0])] + 1
        elif system == "greedy-cc": 
            # Every time through the loop, add the result from calc_marginals to the cand_scores.
            cand_scores = np.add(cand_scores,calc_marginals(candidates, sortable))

    return cand_scores 

def k_borda_winners(x_cand, y_cand, x_vote, y_vote, k):
    '''
    Returns x_win, y_win; two parallel numpy arrays
    containing the coordinates of the candidates with 
    the top Borda scores.
    '''
    assert (len(x_cand) == len(y_cand) and len(x_vote) == len(y_vote))

    cand_scores = get_cand_scores(x_cand,y_cand,x_vote,y_vote,k,"borda",0)

    sorted_permutation = cand_scores.argsort()[:-k-1:-1]
    
    # Extract those candidates using their indices.
    x_win = x_cand[sorted_permutation]
    y_win = y_cand[sorted_permutation]

    return x_win, y_win


def k_approval(x_cand,y_cand,x_vote,y_vote,k): 

    cand_scores = get_cand_scores(x_cand,y_cand,x_vote,y_vote,k,"k-approval",0)
    sorted_permutation = cand_scores.argsort()[:-k-1:-1]
    
    # Extract those candidates using their indices.
    x_win = x_cand[sorted_permutation]
    y_win = y_cand[sorted_permutation]

    return x_win, y_win

def greedy_cc(x_cand,y_cand,x_vote,y_vote,k): 

    # Get top borda scorer 
    cand_scores = get_cand_scores(x_cand,y_cand,x_vote,y_vote,1,"k-borda",0)
    borda = cand_scores.argsort()[-1]
    candidates = [] 
    candidates.append(borda) 
    # Keep looping until we have the total number of candidates that we need
    while len(candidates) < k: 
        cand = get_cand_scores(x_cand,y_cand,x_vote,y_vote,k,"greedy-cc",candidates)
        top_marg = cand.argsort()[-1]
        candidates.append(top_marg)
    
    # Extract those candidates using their indices.
    x_win = x_cand[candidates]
    y_win = y_cand[candidates]

    return x_win,y_win

def calc_marginals(committee, sortable): 
    # This function takes the current composition of the committee and computes a list of marginal scores 
    # based on the committee's current composition. 

    preference = sortable[:,0].tolist()

    # Because I want the lowest index of the committee for each ballot, 
    # I want to start with the index higher than the top candidate. 
    min_index = 101
    for elem in committee: 
        top_index = preference.index(elem) 
        if top_index < min_index: 
            min_index = top_index
    marginals = []
    for i in range(len(preference)): 
        marginals.append(0)
    for i in range(min_index): 
        cand = preference[i]
        # To calculate the marginals, I am adding on whatever difference there is between a candidate's index 
        # and the top preference of committee members. 
        marginals[int(cand)] = marginals[int(cand)] + min_index - i
    return marginals

def main():      
    num_votes = 1000
    x_votes, y_votes = get_2d_gaussian_points(num_votes)

    num_cands = int(num_votes/10)
    x_cands, y_cands = get_2d_gaussian_points(num_cands)

    committee_size = 7

                ## **** COMMENT OUT WHICH TWO YOU DON'T WANT **** ##
    # Compute Borda winners:
    x_win, y_win = k_borda_winners(x_cands, y_cands, x_votes, y_votes, committee_size)

    # # Compute k-approvals: 
    x_win, y_win = k_approval(x_cands, y_cands, x_votes, y_votes, committee_size)

    # # Compute Greedy Chamberlain Courant 
    x_win, y_win = greedy_cc(x_cands,y_cands,x_votes,y_votes,committee_size) 


    # Create plots
    x_win.shape = (-1, 1)
    y_win.shape = (-1, 1)

    # Plot setup
    fig = plt.figure()
    ax = fig.gca()  # Literally: get current axes
    sdvs = 3        # How many standard deviations in plot, larger "zooms out"
    ax.set_title('2D Gaussian Mixture')
    ax.set_xlim(left=-1*sdvs, right=sdvs)
    ax.set_ylim(bottom=-1*sdvs, top=sdvs)

    # Add voters to plot.
    plt.scatter(x_votes, y_votes, s=3, color='blue') # larger s increases point size

    # Add candidates to plot.
    plt.scatter(x_cands, y_cands, s=7, color='red') 

    # Add winners to plot.
    plt.scatter(x_win, y_win, s=128, color='green', marker='o')

    plt.show()

main()