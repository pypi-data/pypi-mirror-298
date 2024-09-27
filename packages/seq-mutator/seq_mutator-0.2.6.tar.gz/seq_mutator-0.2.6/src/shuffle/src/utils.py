

def iter_coherent_overlaps(protein_a, protein_b, min_window=2, margin=0):
    """
    iterate over all overlapping coherent regions of protein_a and protein_b. they must have the same length

    :param protein_a: protein sequence
    :param protein_b: protein sequence
    :param min_window: minimum length of overlapping region

    :return: yields the indices of the overlapping region
    """

    assert len(protein_a) == len(protein_b)

    # iterate over all possible starting points in protein_a and protein_b
    start = 0
    while start < len(protein_a):

        # iterate over all possible lengths of the overlapping region
        end = start
        while end < len(protein_a):

            # if the amino acids at the current positions are not equal, break
            if protein_a[end] != protein_b[end]:
                break
            end += 1

        # if the length of the overlapping region is greater than or equal to min_window, yield the indices
        if end - start >= min_window:

            # apply margin if valid
            yield max(0, start - margin), min(len(protein_a), end + margin)

        # move the start pointer to the next position
        start = end + 1



