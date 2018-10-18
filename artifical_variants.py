#!/usr/bin/env python

__author__="Changbum Hong"
__email__="cb.hong@ngenebio.com"
__modname__="artifical_variants.py"
__created__="2018_10_17"
__company__="ngenebio"

import itertools
import random
import os
import datetime
import pandas as pd
import numpy as np
import sys
import argparse
import time
from HTSeq import FastaReader

BASES = ['A', 'G', 'C', 'T']
TWOBASES = [ ''.join(combo) for combo in itertools.permutations(BASES, 2)]
THREEBASES = [ ''.join(combo) for combo in itertools.permutations(BASES, 3)]

def __main__():
    parser = argparse.ArgumentParser(description='Run make artifical variants(SNVs/InDels)', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_transcript',help='Transcript file(ex, brca1.txt)')
    parser.add_argument('chrom',help='Chromosome number(ex, 17)')
    parser.add_argument('output_vcf',help='Output vcf file (ex, brca1_artifical.vcf)')
    parser.add_argument('ref', help='Spliting FASTA file by chromosome', type=str)
    parser.add_argument('--vartype', help='Type of variant', choices=['SNV','INS','DEL'], type=str, default='SNV')
    args = parser.parse_args()
    print(args.vartype)
    
    run_artifical(args.input_transcript, args.chrom, args.output_vcf, args.vartype, args.ref)

def run_artifical(input_transcript, chrom, output_vcf, vartype, ref):

    raw_df=pd.read_csv(input_transcript,sep="\t")

    tx_exon_dict=dict()

    for i in range(len(raw_df)):
        exon_start_stop = zip(map(int,raw_df["Exon Starts"][i].split(",")),map(int, raw_df["Exon Stops"][i].split(",")))
        tx_exon_dict[raw_df["Transcript Name"][i]]= exon_start_stop

    expanded_tx_exon_dict=dict()
    for tx_name, exon_coordinate_list in tx_exon_dict.items():
        new_coordiante_list=[]
        for start, stop in exon_coordinate_list:
            new_start=start-100
            new_stop=stop+100
            new_coordiante_list.append((new_start, new_stop))
        expanded_tx_exon_dict[tx_name] = new_coordiante_list
    print("Raw data: ")
    print(expanded_tx_exon_dict)
    print("\n\n")

    interval_list=[]
    [interval_list.extend(x) for x in expanded_tx_exon_dict.values()]

    sorted_by_start=sorted(interval_list,key=lambda x: x[0])

    collapsed_interval_list = list(collapse_intervals(sorted_by_start))
    print("Before collapsing we have: " + str(len(interval_list)) + " intervals")
    print("After collapsing we have: " + str(len(collapsed_interval_list)) + " intervals")
    print("\nOur new interval set:\n")
    print(collapsed_interval_list)

    col_names= ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER','INFO']
    variant_df = pd.DataFrame(columns=col_names)
    
    spinner = spinning_cursor()
    
    for interval in collapsed_interval_list:
        pos, stop = interval
        while(pos < stop):
            var_dict = get_variants(chrom, pos, vartype, ref)
            variant_df = variant_df.append(var_dict)
            pos += 1
             
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            #time.sleep(0.1)
            sys.stdout.write('\b')
    
    vcf_header = """##fileformat=VCFv4.2
##FILTER=<ID=PASS,Description="All filters passed">
##reference=GrCh37
##contig=<ID=chr17,length=81195210>
##contig=<ID=chr13,length=115169878>
"""
    
    vcf_header = vcf_header.format(datetime.datetime.utcnow().strftime("%Y%m%d"))
    '\n'.join([vcf_header, ('\t'.join(variant_df.columns)), '\t'.join(col_names)])
    
    try:
        os.remove(output_vcf)
    except OSError:
        pass
    
    f=open(output_vcf,'a')
    f.write(vcf_header)
    variant_df.to_csv(f, sep='\t', na_rep='.', index=False)
    
    print("done! check %s file"%(output_vcf))    


def collapse_intervals(intervals):
    cur_start, cur_stop = intervals[0]
    for next_start, next_stop in intervals[1:]:
        if cur_stop < next_start:
            yield cur_start, cur_stop
            cur_start, cur_stop = next_start, next_stop
        else:
            cur_stop = next_stop
    yield cur_start, cur_stop


def get_variants(chr, pos,vartype, fasta_chr_file):
    variant_list = []
    #fasta_chr_file="/NGENEBIO/workflow-dependencies/seqseek/homo_sapiens_GRCh37/chr%s.fa"%(chr)
    ref_seq = FastaReader(fasta_chr_file).__iter__().next()
    ref = ref_seq[pos-1:pos+3].seq.upper()

    if vartype=='SNV':
       variant_list.extend(get_snps(chr, pos, ref))
    if vartype=='DEL':
       variant_list.extend(get_insertions(chr, pos, ref))
    if vartype=='INS':
       variant_list.extend(get_deletions(chr, pos, ref))
    return variant_list

def get_snps(chr, pos, ref):
    snp_list = []
    ref = ref[0]
    chr = 'chr%s'%chr
    for base in BASES:
        if base == ref: continue
        snp_list.append({'#CHROM': chr, 'POS': pos, 'REF': ref, 'ALT': base})
    return snp_list

def get_insertions(chr, pos, ref):
    ins_list = []
    ref = ref[0]
    for base in itertools.chain(BASES, random.sample(TWOBASES, 2), random.sample(THREEBASES, 2)):
        ins_list.append({'#CHROM': chr, 'POS': pos,'REF': ref[0], 'ALT': ref[0] + base})
    return ins_list

def get_deletions(chr, pos, ref):
    del_list = []
    del_list.append({'#CHROM': chr, 'POS': pos, 'REF': ref[0:2], 'ALT': ref[0]})
    del_list.append({'#CHROM': chr, 'POS': pos, 'REF': ref[0:3], 'ALT': ref[0]})
    del_list.append({'#CHROM': chr, 'POS': pos, 'REF': ref, 'ALT': ref[0]})
    return del_list

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

if __name__=="__main__": __main__()
