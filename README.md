# Artifical Variants

[![Build Status](https://travis-ci.org/hongiiv/artifical_variants.svg?branch=master)](https://travis-ci.org/hongiiv/artifical_variants)
[![codecov](https://codecov.io/gh/hongiiv/artifical_variants/branch/master/graph/badge.svg)](https://codecov.io/gh/hongiiv/artifical_variants)
[![CRAN
status](http://www.r-pkg.org/badges/version/usethis)](https://cran.r-project.org/package=usethis)
[![lifecycle](https://img.shields.io/badge/lifecycle-stable-brightgreen.svg)](https://www.tidyverse.org/lifecycle/#stable)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://GitHub.com/hongiiv/artifical_variants/issues/)

Make artifical variants(SNVs/InDels))

#### Prerequisites

* Split FASTA into seperate files by chromsome (ex, chr1.fa)
* Python library (requirements.txt)
 * pandas
 * numpy
 * HTSeq

#### Install

`git clone https://github.com/hongiiv/artifical_variants.git`

#### Run

BRCA1 all missense mutations and ±100 bp intron. All BRCA1 transcripts are collapse intervals.

`$ python artifical_variants.py brca1.txt 17 brca1_artifical.vcf /NGENEBIO/workflow-dependencies/seqseek/homo_sapiens_GRCh37/chr17.fa`

BRCA2 

`$ python artifical_variants.py brca2.txt 13 brca2_artifical.vcf /NGENEBIO/workflow-dependencies/seqseek/homo_sapiens_GRCh37/chr13.fa`

	$ python artifical_variants.py --help
	usage: artifical_variants.py [-h] [--vartype {SNV,INS,DEL}]
	                             input_transcript chrom output_vcf ref

	Run make artifical variants(SNVs/InDels)

	positional arguments:
	  input_transcript      Transcript file(ex, brca1.txt)
	  chrom                 Chromosome number(ex, 17)
	  output_vcf            Output vcf file (ex, brca1_artifical.vcf)
	  ref                   Spliting FASTA file by chromosome

	optional arguments:
 	 -h, --help            show this help message and exit
 	 --vartype {SNV,INS,DEL}
  	                      Type of variant (default: SNV)
