"""abmatrix.py"""

import os
import zipfile
from urllib.parse import urlparse
from io import StringIO, BytesIO
from collections import OrderedDict
import boto3
from pywisdom.absample import AbSample
from pywisdom.ablocus import AbLocus
from pywisdom.abheader import AbHeader


class EmptyMatrix(Exception):
    """Custom Exception for empty AB Matrix data set"""


class MisalignedLoci(Exception):
    """Incorrect locus index"""

    def __init__(self, message):
        self.message = message


class SampleNotFound(Exception):
    """Requested sample identifier not found in AB Matrix data set"""

    def __init__(self, message):
        self.message = message


class LocusNotFound(Exception):
    """Requested locus identifier not found in AB Matrix data set"""

    def __init__(self, message):
        self.message = message


class BadABFormat(Exception):
    """Bad input AB Matrix format"""

    def __init__(self, message):
        self.message = message


class AbMatrix:
    """Python class to parse, store and manipulate AB Matrix data"""

    # Initialize AB Matrix data structure
    def __init__(self):
        self._filename = ""
        self._iszip = False
        self._s3_input = False
        self._has_data = False
        self._header = AbHeader()
        self._index = OrderedDict()
        self._sample_index = OrderedDict()
        self._num_samples = 0
        self._num_loci = 0
        self._fstream = None

    def close(self):
        """Close ABMatrix file stream and reset data

        If used on an already empty data set, nothing happens

        Returns
        -------

        None

        """
        if self._has_data:
            self._filename = ""
            self._iszip = False
            self._has_data = False
            self._s3_input = False
            self._header = AbHeader()
            self._index = OrderedDict()
            self._sample_index = OrderedDict()
            self._num_samples = 0
            self._num_loci = 0
            self._fstream.close()
            del self._fstream
        else:
            pass

    def get_header(self):
        """Get AB Matrix header

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        AbHeader instance for AB Matrix file

        """
        if not self._has_data:
            raise EmptyMatrix
        else:
            return self._header

    def set_header(self, header):
        """Populate or replace AB Matrix header

        Parameters
        ----------

        header : AbHeader
            AbHeader class instance

        Returns
        -------

        None

        """
        self._header = header

    def fetch_locus(self, locusid):
        """Fetch genotypes for a requested locus

        Parameters
        ----------

        locusid : string
            identifier of locus to retrieve

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        KeyError
            locus identifier not found

        MisalignedLoci
            misalignment of data structures

        Returns
        -------

        AbLocus instance with requested locus data

        """
        if not self._has_data:
            raise EmptyMatrix
        try:
            offset = self._index[locusid]
        except KeyError as e:
            raise LocusNotFound(f"Requested locus: {locusid}") from e
        self._fstream.seek(offset)
        line = self._fstream.readline()
        if self._iszip:
            line = line.decode("utf-8")
        locus_array = line.rstrip().split("\t")
        locus = locus_array.pop(0)
        requested_locus = AbLocus()
        if locus != locusid:
            raise MisalignedLoci(locus)
        else:
            requested_locus.set_id(locusid)
            requested_locus.set_genotypes(locus_array)
            return requested_locus

    def fetch_sample(self, sampleid):
        """Fetch genotypes for a requested sample

        Parameters
        ----------

        sampleid : string
            identifier of sample to retrieve

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        AbSample instance with requested sample data

        """
        if not self._has_data:
            raise EmptyMatrix
        try:
            index = self._sample_index[sampleid]
        except KeyError as e:
            raise SampleNotFound(f"Requested sample: {sampleid}") from e
        requested_sample = AbSample()
        requested_sample.set_id(sampleid)
        gt_array = []
        for offset in self._index.values():
            self._fstream.seek(offset)
            line = self._fstream.readline()
            if self._iszip:
                line = line.decode("utf-8")
            locus_array = line.rstrip().split("\t")[1:]
            gt_array.append(locus_array[index])
        requested_sample.set_genotypes(gt_array)
        return requested_sample

    def iter_loci(self):
        """Generator to iterate loci in AB Matrix data set

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        MisalignedLoci
            misalignment of data structures

        Returns
        -------

        iterator to instance of AbLocus class

        """
        if not self._has_data:
            raise EmptyMatrix
        for locus, offset in self._index.items():
            current_locus = AbLocus()
            current_locus.set_id(locus)
            self._fstream.seek(offset)
            line = self._fstream.readline()
            if self._iszip:
                line = line.decode("utf-8")
            locus_array = line.rstrip().split("\t")
            locusid = locus_array.pop(0)
            if locusid != locus:
                raise MisalignedLoci(locusid)
            else:
                current_locus.set_genotypes(locus_array)
                yield current_locus

    def iter_samples(self):
        """Generator to iterate samples in AB Matrix data set

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        iterator to instance of AbSample class

        """
        if not self._has_data:
            raise EmptyMatrix
        for sample, index in self._sample_index.items():
            current_sample = AbSample()
            current_sample.set_id(sample)
            gt_array = []
            for offset in self._index.values():
                self._fstream.seek(offset)
                line = self._fstream.readline()
                if self._iszip:
                    line = line.decode("utf-8")
                locus_array = line.rstrip().split("\t")[1:]
                gt_array.append(locus_array[index])
            current_sample.set_genotypes(gt_array)
            yield current_sample

    def sample_uppercase(self):
        """Convert sample identifiers to uppercase

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        None

        """
        if self._has_data:
            sample_list = list(self._sample_index.keys())
            translate = {x: x.upper() for x in sample_list}
            new_sample_index = OrderedDict()
            for key, val in self._sample_index.items():
                new_sample_index[translate[key]] = val
            self._sample_index = new_sample_index
        else:
            raise EmptyMatrix

    def rename_samples(self, translate):
        """Rename sample identifiers

        Parameters
        ----------

        translate : dict
            dictionary with rename specification, e.g., {'original1':'new1', 'original2':'new2'}

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        TypeError
            argument is not a dictionary type

        Returns
        -------

        None

        """
        if self._has_data:
            if isinstance(translate, dict):
                new_sample_index = OrderedDict()
                for key, val in self._sample_index.items():
                    if key in translate:
                        new_id = translate[key]
                        new_sample_index[new_id] = val
                    else:
                        new_sample_index[key] = val
                self._sample_index = new_sample_index
            else:
                raise TypeError
        else:
            raise EmptyMatrix

    def locus_list(self):
        """Fetch list of locus identifiers in AB Matrix data set

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        list of locus identifiers

        """
        if self._has_data:
            return list(self._index.keys())
        else:
            raise EmptyMatrix

    def drop_samples(self, sample_list):
        """Remove sample(s) from the AB data set

        Parameters
        ----------

        sample_list : list
            list of sample identifiers to drop

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        SampleNotFound
            requested sampleid(s) not found in AB data set

        TypeError
            Argument is not a list

        Returns
        -------

        None

        """
        if self._has_data:
            if isinstance(sample_list, list):
                for sid in sample_list:
                    if sid not in self._sample_index:
                        raise SampleNotFound(f"Requested sample: {sid}")
                for sid in sample_list:
                    self._sample_index.pop(sid)
                ns = len(list(self._sample_index.keys()))
                self._num_samples = ns
                self._header.set("Num Samples", ns)
                self._header.set("Total Samples", ns)
            else:
                raise TypeError
        else:
            raise EmptyMatrix

    def read(self, filename):
        """Read data into initialized AB Matrix

        Parameters
        ----------

        filename : string
            input AB Matrix file name

        Raises
        ------

        FileNotFoundError
            unable to open input AB Matrix file

        BadABFormat
            Bad input AB Matrix format

        Returns
        -------

        None

        """
        if filename.startswith("s3://"):
            self._s3_input = True
            o = urlparse(filename)
            if o.path.startswith("/"):
                s3_key = o.path.lstrip("/")
            else:
                s3_key = o.path
            s3 = boto3.client("s3")
            content = s3.get_object(Bucket=o.netloc, Key=s3_key)["Body"].read()
            if filename.endswith(".zip"):
                self._iszip = True
                zipbase = os.path.basename(".".join(filename.split(".")[:-1]))
                buffer = BytesIO(content)
                zipstream = zipfile.ZipFile(buffer)
                self._fstream = zipstream.open(zipbase, "r")
            else:
                self._fstream = StringIO(content.decode("utf-8"))
        elif os.path.isfile(filename):
            self._filename = filename
            if zipfile.is_zipfile(filename):
                self._iszip = True
                zipstream = zipfile.ZipFile(filename, "r")
                zipbase = os.path.basename(".".join(filename.split(".")[:-1]))
                self._fstream = zipstream.open(zipbase, "r")
            else:
                self._fstream = open(filename, "r", encoding="utf-8")
        else:
            raise FileNotFoundError
        is_header = True
        wait_sample = False
        offset = 0
        lineno = 0
        line = self._fstream.readline()
        if self._iszip:
            line = line.decode("utf-8")
        lineno += 1
        if not line.startswith("[Header]"):
            raise BadABFormat("First line does not have [Header]")
        line = self._fstream.readline()
        lineno += 1
        while line:
            if self._iszip:
                line = line.decode("utf-8")
            if is_header:
                if line.startswith("[Data]"):
                    wait_sample = True
                elif wait_sample:
                    sample_list = line.rstrip().split("\t")[1:]
                    for pos, sample in enumerate(sample_list):
                        self._sample_index[sample] = pos
                    is_header = False
                    wait_sample = False
                    offset = self._fstream.tell()
                    self._num_samples = len(sample_list)
                else:
                    entry = line.rstrip().split("\t")
                    if len(entry) < 2:
                        raise BadABFormat(f"Bad header entry line {lineno}")
                    elif len(entry) > 2:
                        nread = 0
                        key = ""
                        value = ""
                        for elem in entry:
                            if len(elem) > 1:
                                if nread < 1:
                                    key = elem
                                    nread += 1
                                else:
                                    value = elem
                                    break
                        self._header.set(key, value)
                    else:
                        self._header.set(entry[0], entry[1])
            else:
                self._num_loci += 1
                locus_line = line.rstrip().split("\t")
                locus_id = locus_line.pop(0)
                if len(locus_line) != self._num_samples:
                    raise BadABFormat(f"Wrong number of genotypes line {lineno}")
                self._index[locus_id] = offset
                offset = self._fstream.tell()
            line = self._fstream.readline()
            lineno += 1
        self._has_data = True

    def sample_list(self):
        """Fetch sample identifiers in AB Matrix data set

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        list of sample identifiers

        """
        if self._has_data:
            return list(self._sample_index.keys())
        else:
            raise EmptyMatrix

    def write(self, filename, zippit=False):
        """Write in-memory AB Matrix data set to file

        About genotypes data

        Parameters
        ----------

        filename : string
            name of file to write output

        zippit : bool
            output file is zip compressed

        Raises
        ------

        FileNotFoundError
            unable to open input AB Matrix file

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        None

        """
        if not self._has_data:
            raise EmptyMatrix

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[Header]{os.linesep}")
            for key, value in self._header.iter_items():
                f.write(f"{key}\t{value}{os.linesep}")
            f.write(f"[Data]{os.linesep}")
            sample_list = list(self._sample_index.keys())
            sample_header = "\t".join(sample_list)
            f.write(f"\t{sample_header}{os.linesep}")
            for locusid, offset in self._index.items():
                self._fstream.seek(offset)
                line = self._fstream.readline()
                if self._iszip:
                    line = line.decode("utf-8")
                locus_array = line.rstrip().split("\t")
                _ = locus_array.pop(0)
                f.write(locusid)
                for pos in self._sample_index.values():
                    f.write(f"\t{locus_array[pos]}")
                f.write(os.linesep)
        if zippit:
            arcname = f"{filename}.zip"
            with zipfile.ZipFile(arcname, "w") as f:
                f.write(filename)

    def num_loci(self):
        """Fetch number of loci in AB Matrix data set

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        Integer representing number of loci

        """
        if self._has_data:
            return self._num_loci
        else:
            raise EmptyMatrix

    def num_samples(self):
        """Fetch number of samples in AB Matrix data set

        Raises
        ------

        EmptyMatrix
            AbMatrix class has no data

        Returns
        -------

        Integer representing number of samples

        """
        if self._has_data:
            return self._num_samples
        else:
            raise EmptyMatrix
