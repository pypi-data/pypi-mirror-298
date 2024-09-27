import itertools

from .restriction_enzyme_hit import RestrictionEnzymeHit


class RestrictionSiteFinder:
    """
    Find restriction enzyme sites in a protein sequence
    """

    def __init__(self, codon_table, restriction_batch):
        self.codon_table = codon_table
        self.restriction_batch = restriction_batch

        self.ambiguity_codes = {
            "V": ["G", "A", "C"],
            "N": ["A", "T", "G", "C"],
            "Y": ["T", "C"],
            "R": ["A", "G"]
        }

    def _get_all_possible_dna(self, site):
        """
        get all possible DNA sequences for a given dna site. This is used to handle ambiguity codes.
        Imagine a site "R" which can be either "A" or "G". This function will return both
        possibilities and combine them with the other sites.

        :param site: dna site (str)

        :return: list of all possible DNA sequences given the ambiguity codes
        """
        dnas = []

        for base in site:
            if base in self.ambiguity_codes:
                new_base = self.ambiguity_codes[base]
                dnas.append(new_base)
            else:
                dnas.append([base])

        # return all possible combinations of the dna sites
        return ["".join(dna) for dna in itertools.product(*dnas)]

    def _make_translatable(self, site):
        """
        make a site translatable by adding missing nucleotides. This is used to handle
        sites that are not devidable by 3. For example, a site "GATT" is not devidable by 3:
        This funktion will append "N" to the site to make it devidable by 3.

        :param site: dna site

        :return: all possible translatable sites
        """
        overstanding_ns = len(site) % 3

        if not overstanding_ns:
            return [site]

        if overstanding_ns == 2:
            return [site + "N", "N" + site]

        # overstanding_ns == 1
        return [site + "NN", "N" + site + "N", "NN" + site]

    def find_enzyme_hits(self, sequence: str, start=0):
        """
        find all possible restriction enzyme hits in a protein sequence

        :param sequences: aligned protein sequences
        :param start: start position of the protein sequence

        :return hits: list of restriction enzyme hits
        """
        hits = []

        # iterate over all reading frames
        for enzyme in self.restriction_batch:

            # get the site and all the combinations of the site, that can be translated
            sites = self._make_translatable(enzyme.site)
            site_length = int(len(sites[0]) / 3)

            possible_dnas = map(self._get_all_possible_dna, sites)
            possible_dnas = list(itertools.chain(*possible_dnas))

            # compare the site with stepwise with the sequence
            for i in range(len(sequence) + 1 - site_length):

                # reading_frame = sequences[0][i:i + site_length]
                reading_frame = sequence[i:i + site_length]

                # filter dna sequences that can be translated to a reading frame
                matching_dnas = [
                    dna for dna in possible_dnas if self.codon_table.translate(dna) == reading_frame]

                # if there are matching dnas, create a hit and append it to the hits
                if matching_dnas:
                    hit = RestrictionEnzymeHit(reading_frame, enzyme, matching_dnas, start + i)
                    hits.append(hit)

        return hits


