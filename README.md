# Artifical Variants

Make artifical variants(SNVs/InDels))

BRCA1 

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