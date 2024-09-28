"""absample.py"""


class AbSample:
    """Python class to store and manipulate AB Matrix sample data"""

    # Initialize AbSample data structure
    def __init__(self):
        self._genotypes = None
        self._id = ""

    def set_id(self, sampleid):
        """Set sample identifier string

        Parameters
        ----------

        sampleid : string
            sample identifier string

        Returns
        -------

        None

        """
        self._id = sampleid

    def get_id(self):
        """Get sample identifier string

        Returns
        -------

        Sample identifier string

        """
        return self._id

    def set_genotypes(self, gtarray):
        """Populate sample genotype list

        Parameters
        ----------

        gtarray : list
            list of genotypes associated with the sample

        Returns
        -------

        None

        """
        self._genotypes = gtarray

    def get_genotypes(self):
        """Get list of sample genotypes

        Returns
        -------

        List of sample genotypes

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

    def concordance(self, target, missing=True):
        """Get counts of concordant sites between two AbSample instances

        Parameters
        ----------

        missing : boolean
            should analysis include missing genotypes (default: True)

        Returns
        -------

        Tuple of counts of concordant genotypes and total genotypes

        """
        n_concordant = 0
        n_total = 0
        target_genotypes = target.get_genotypes()
        for i, gt in enumerate(self._genotypes):
            target_gt = target_genotypes[i]
            if missing:
                n_total += 1
                if gt == target_gt:
                    n_concordant += 1
            else:
                if (gt != "--") and (target_gt != "--"):
                    n_total += 1
                    if gt == target_gt:
                        n_concordant += 1
        return (n_concordant, n_total)
