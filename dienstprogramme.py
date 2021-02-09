# von https://stackoverflow.com/questions/2460177/edit-distance-in-python
def levenshtein_distanz(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distanzen = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distanzen_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distanzen_.append(distanzen[i1])
            else:
                distanzen_.append(1 + min((distanzen[i1], distanzen[i1 + 1], distanzen_[-1])))
        distanzen = distanzen_
    return distanzen[-1]
