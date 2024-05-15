CODE_TO_GCBO = {}


def map_to_gcbo(terms):
    mapped = []
    for term in terms:
        if term.label in CODE_TO_GCBO:
            mapped.append(CODE_TO_GCBO[term.label])
    return mapped
