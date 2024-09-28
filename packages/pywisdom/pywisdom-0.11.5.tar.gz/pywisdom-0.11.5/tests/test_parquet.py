"""test_parquet.py"""

import os
from collections import Counter
import pyarrow.parquet as pq
import pyarrow.compute as pc

input_parquet = os.path.expanduser(
    "~/git/popgendad/pywisdom/tests/test_subset_input.parquet"
)
raw_tbl = pq.read_table(input_parquet)
smplist = raw_tbl.column("sampleid")
expr = pc.field("sampleid").isin(["EJZGPRF", "EBTYJDG", "ETNLGRB", "EQVMPYG"])
filt_tbl = raw_tbl.filter(expr)
gt_tbl = filt_tbl.drop("sampleid")
for lid in gt_tbl.column_names:
    lcs = gt_tbl.column(lid)
    bins = Counter([x.as_py() for x in lcs.combine_chunks()])
    af = (bins[0] + bins[1]) / (bins[0] + bins[1] + bins[2])
    hom = 1.0 - (2.0 * af * (1.0 - af))
    print(f"{lid},{hom}")
