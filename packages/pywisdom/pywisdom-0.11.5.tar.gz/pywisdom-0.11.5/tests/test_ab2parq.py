"""ab2parq.py"""

import sys
import pyarrow as pa
import pyarrow.parquet as pq

if len(sys.argv) < 3:
    print("Usage: ab2parq.py <input_ab> <output_parquet")
    sys.exit(8)
input_ab = sys.argv[1]
output_parquet = sys.argv[2]
with open(input_ab, "r", encoding="utf-8") as f:
    while True:
        line = f.readline()
        if line.startswith("[Data]"):
            sample_header = next(f)
            sample_list = sample_header.rstrip().split("\t")[1:]
            break
    table = pa.Table.from_arrays([pa.array(sample_list)], names=["id"])
    for line in f:
        geno_list = line.rstrip().split("\t")
        locusid = geno_list.pop(0)
        table = table.append_column(locusid, [pa.array(geno_list)])
    pq.write_table(table, output_parquet)
