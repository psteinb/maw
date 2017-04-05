#!/usr/bin/env python3
import sys

import numpy as np

from multiprocessing import cpu_count, Pool

np.random.seed(2017)

def generate(total_count,alphabet=list("ACGTN")):

    npalphabet = np.array(alphabet)
    sample = np.random.choice(npalphabet, total_count)

    return "".join(sample.tolist())

def produce_chunks(n_bp,n_cores,alphabet):

    partitions = [ ]
    for i in range(n_cores):
        partitions.append(int(n_bp/n_cores))

    pool = Pool(processes=n_cores)
    counts=pool.map(generate, partitions)

    return counts

if __name__=='__main__':

    ncores = cpu_count()

    n_bp = 100
    if len(sys.argv) > 1:
        n_bp = int(float(sys.argv[1]))
        if "-h" in sys.argv or "--help" in sys.argv:
            print(""" app to synthesize fasta files with a random distribution drawn from an alphabet ("ACGTN" by default)\n
            usage: python3 synthesize_DNA.py <number of bp to generate|default: 100>""")
            sys.exit(1)

    partitions = [ int(n_bp/ncores) for item in range(ncores)]

    sizeof = np.dtype(np.int8).itemsize

    chunks = produce_chunks(n_bp,ncores, alphabet = list("ACGTN"))

    counter = 0
    for c in chunks:
        print(">",counter)
        print(c)
        counter += 1
    #print("[parallel version] required memory %.3f MB" % (n_bp*sizeof*3/(1024*1024)))
