import numpy as np


def num_of_diff_votes(election):
    if election.fake:
        return {'value': None}

    str_votes = [str(vote) for vote in election.votes]
    return {'value': len(set(str_votes))}


def voterlikeness_sqrt(election):
    if election.fake:
        return {'value': None}

    vectors = election.votes_to_voterlikeness_vectors()
    score = 0.
    for vector in vectors:
        for value in vector:
            score += value**0.5
    return {'value': score}


def voterlikeness_harmonic(election):
    if election.fake:
        return {'value': None}

    vectors = election.votes_to_voterlikeness_vectors()
    score = 0.
    for vector in vectors:
        vector = sorted(vector)
        for pos, value in enumerate(vector):
            score += 1/(pos+2)*value
    return {'value': score}


def borda_diversity(election):
    if election.fake:
        return {'value': None}

    vector = np.array(election.votes_to_bordawise_vector())
    return {'value': np.std(vector)}
