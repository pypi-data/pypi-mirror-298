"""test_methods.py"""

from pywisdom.abmatrix import AbMatrix

ab = AbMatrix()
ab.read("test_input.ab")
trans = {"BSNRPVD": "bsnrpvd"}
ab.rename_samples(trans)
ab.drop_samples(["EQVMPYG", "EHNCBGX", "EJCVKLZ", "EZGDFSV", "ENYGTRF"])
ab.write("mytest.ab")
ab.close()
