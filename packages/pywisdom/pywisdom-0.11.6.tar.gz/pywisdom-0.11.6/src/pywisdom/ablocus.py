"""ablocus.py"""

from collections import Counter


class AbLocus:
    """Python class to store and manipulate AB Matrix locus data"""

    # Initialize AB Locus data structure
    def __init__(self):
        self._genotypes = None
        self._id = ""

    def set_id(self, locusid):
        """Set locus identifier string

        Parameters
        ----------

        locusid : string
            locus identifier string

        Returns
        -------

        None

        """
        self._id = locusid

    def get_id(self):
        """Get locus identifier string

        Returns
        -------

        Locus identifier string

        """
        return self._id

    def set_genotypes(self, gtarray):
        """Populate locus genotype list

        Parameters
        ----------

        gtarray : list
            list of genotypes associated with the locus

        Returns
        -------

        None

        """
        self._genotypes = gtarray

    def get_genotypes(self):
        """Get list of locus genotypes

        Returns
        -------

        List of locus genotypes

        """
        return self._genotypes

    def get_missing(self):
        """Get counts of missing genotypes

        Returns
        -------

        Tuple of counts of missing genotypes and total genotypes

        """
        n_missing = 0
        n_total = 0
        for gt in self._genotypes:
            n_total += 1
            if gt == "--":
                n_missing += 1
        return (n_missing, n_total)

    def count_genotypes(self):
        """Get counts of all genotypes at locus

        Returns
        -------

        Dictionary keyed on genotype with counts as values
        """
        return dict(Counter(self._genotypes))
