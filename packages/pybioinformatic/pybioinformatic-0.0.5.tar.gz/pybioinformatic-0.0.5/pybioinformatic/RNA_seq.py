"""
File: RNA_seq.py
Description: Command line util.
CreateDate: 2024/7/24
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import TextIOWrapper
from collections import defaultdict
from os import makedirs, getcwd
from os.path import abspath
from shutil import which
from natsort import natsort_key
from click import echo


def parse_sample_info(sample_info: TextIOWrapper) -> dict:
    d = defaultdict(list)  # {sample_name: [fastq_file1, fastq_file2], ...}
    for line in sample_info:
        split = line.strip().split('\t')
        d[split[0]].append(split[1])
    return d


class MergeSamples:
    def __init__(self,
                 hisat2_bam: set,
                 stringtie_gtf: set):
        self.hisat2_bam = hisat2_bam
        self.stringtie_gtf = stringtie_gtf


class SpecificStrandRNASeqAnalyser:
    """
    Single sample specific strand transcriptome analyser.
    """
    def __init__(self,
                 read1: str,
                 read2: str,
                 ref_genome: str,
                 output_path: str,
                 num_threads: int = 10,
                 ref_gff: str = None,
                 sample_name: str = None):
        self.read1 = abspath(read1)
        self.read2 = abspath(read2)
        self.ref_genome = abspath(ref_genome)
        if ref_gff:
            self.ref_gff = abspath(ref_gff)
            self.gff_to_gtf()
        else:
            self.ref_gff = None
            self.ref_gtf = None
        self.num_threads = num_threads
        self.output_path = abspath(output_path)
        if sample_name is None:
            self.sample_name = self.read1.split('/')[-1].split('.')[0]
        else:
            self.sample_name = sample_name

    def gff_to_gtf(self,
                   gffread_exe: str = 'gffread'):
        if self.ref_gff is None:
            echo(f'\33[31mError: Invalid reference genome annotation file "{self.ref_gff}".\033[0m', err=True)
        gffread_exe = which(gffread_exe)
        gtf = '.'.join(self.ref_gff.split('.')[:-1]) + '.gtf'
        cmd = f"{gffread_exe} {self.ref_gff} -T -o {gtf}"
        self.ref_gtf = gtf
        return cmd

    @staticmethod
    def __other_options(options_dict: dict, command: str):
        for option, value in options_dict.items():
            if len(option) == 1:
                command += f'-{option} {value} '
            else:
                command += f'--{option} {value} '
        return command

    def run_fastp(self,
                  q_value: int = 20,
                  fastp_exe: str = 'fastp',
                  **kwargs) -> str:
        """
        \n\nRaw reads quality control.
        \n\033[1m:param:\033[0m
        fastp_exe: fastp executable file path. (type=str)
        q_value: Minimum quality value of base. (type=int, default=20)
        kwargs: Other options of fastp.
        \n\033[1m:return:\033[0m
        Fastp command. (type=str)
        """
        fastp_exe = which(fastp_exe)  # Get fastp executable file absolute path.
        out_path = f'{self.output_path}/01.QC/{self.sample_name}'
        makedirs(out_path, exist_ok=True)
        if self.read2:
            cmd = f"{fastp_exe} " \
                  f"-w {self.num_threads} " \
                  f"-q {q_value} " \
                  f"-i {self.read1} " \
                  f"-I {self.read2} " \
                  f"-o {out_path}/{self.sample_name}_R_clean.fq.gz " \
                  f"-O {out_path}/{self.sample_name}_F_clean.fq.gz " \
                  f"-j {out_path}/{self.sample_name}.fastp.json " \
                  f"-h {out_path}/{self.sample_name}.fastp.html "
            self.clean1 = f'{out_path}/{self.sample_name}_R_clean.fq.gz'
            self.clean2 = f'{out_path}/{self.sample_name}_F_clean.fq.gz'
        else:
            cmd = f"{fastp_exe} -w {self.num_threads} -q {q_value} -i {self.read1} -o {out_path}/{self.sample_name}_clean.fq.gz "
            self.clean1 = f'{out_path}/{self.sample_name}_clean.fq.gz'
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd

    def run_hisat2(self,
                   build_index: bool = False,
                   hisat2_exe: str = 'hisat2',
                   samtools_exe: str = 'samtools',
                   storer: MergeSamples = None,
                   **kwargs):
        cmd = ''
        hisat2_exe = which(hisat2_exe)
        samtools_exe = which(samtools_exe)
        out_path = f'{self.output_path}/02.mapping/{self.sample_name}'
        makedirs(out_path, exist_ok=True)
        if build_index:
            cmd += f"{hisat2_exe}-build -x {self.ref_genome} {self.ref_genome}\n"
        cmd += f"{hisat2_exe} " \
               f"--rna-strandness RF " \
               f"-p {self.num_threads} " \
               f"-x {self.ref_genome} " \
               f"-1 {self.clean1} " \
               f"-2 {self.clean2} " \
               f"--summary-file {out_path}/{self.sample_name}.ht2.log | " \
               f"{samtools_exe} sort " \
               f"-@ {self.num_threads} " \
               f"-T {self.sample_name} - > {out_path}/{self.sample_name}.ht2.sort.bam "
        self.sort_bam = f'{out_path}/{self.sample_name}.ht2.sort.bam'
        if storer:
            storer.hisat2_bam.add(f'{out_path}/{self.sample_name}.ht2.sort.bam')
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd

    def run_stringtie(self,
                      stringtie_exec: str = 'stringtie',
                      storer: MergeSamples = None,
                      **kwargs):
        stringtie_exec = which(stringtie_exec)
        out_path = f'{self.output_path}/03.assembly/{self.sample_name}'
        makedirs(out_path, exist_ok=True)
        cmd = f"{stringtie_exec} " \
              f"--rf " \
              f"-p {self.num_threads} " \
              f"-o {out_path}/{self.sample_name}.st.gtf " \
              f"-l {self.sample_name} " \
              f"{self.sort_bam} "
        if storer:
            storer.stringtie_gtf.add(f'{out_path}/{self.sample_name}.st.gtf')
        if self.ref_gff:
            cmd += f"-G {self.ref_gff} "
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd

    def run_stringtie_merge(self,
                            gtf_list: list,
                            m: int = 200,
                            c: float = 1.0,
                            F: float = 0.5,
                            g: int = 0,
                            stringtie_exec: str = 'stringtie',
                            **kwargs):
        stringtie_exec = which(stringtie_exec)
        out_path = f'{self.output_path}/03.assembly'
        makedirs(out_path, exist_ok=True)
        gtf_list.sort(key=natsort_key)
        gtf_files = ' '.join(gtf_list)
        cmd = f"{stringtie_exec} --merge " \
              f" -p {self.num_threads} " \
              f"-m {m} -c {c} -F {F} -g {g} " \
              f"-o {out_path}/All.stringtie.gtf " \
              f"{gtf_files} "
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd

    def run_cuffcompare(self,
                        cuffcompare_exe: str = 'cuffcompare',
                        gffread_exe: str = 'gffread_exe'):
        cuffcompare_exe = which(cuffcompare_exe)
        out_path = f'{self.output_path}/03.assembly'
        makedirs(out_path, exist_ok=True)
        cwd = getcwd()
        gff_to_gtf = self.gff_to_gtf(gffread_exe=gffread_exe)
        mv = f"mv {cwd}/cuffcompare.* {out_path}/"
        extract_gtf = fr'''awk -F'\t' '$3~/[uxijo]/' {out_path}/cuffcompare.All.stringtie.gtf.tmap | cut -f 5 | grep -f - {out_path}/cuffcompare.combined.gtf | awk -F'\t' '$7 != "."' > {out_path}/novel_transcript.gtf'''
        extract_novel_transcript_seq = (
            f"{gffread_exe} -g {self.ref_genome} -w {out_path}/novel_transcript.fa {out_path}/novel_transcript.gtf\n"
            f"{gffread_exe} -g {self.ref_genome} -x {out_path}/novel_transcript_pep.fa {out_path}/novel_transcript.gtf"
        )
        merge_gtf = f"cat {self.ref_gtf} {out_path}/novel_transcript.gtf > {out_path}/All.gtf"
        cmd = (f"{gff_to_gtf}\n"
               f"{cuffcompare_exe} -r {self.ref_gtf} -R -o cuffcompare {out_path}/All.stringtie.gtf\n{mv}\n"
               f"{extract_gtf}\n"
               f"{extract_novel_transcript_seq}\n"
               f"{merge_gtf}")
        self.ref_gtf = f'{out_path}/All.gtf'
        return cmd

    def run_featureCounts(self,
                          bam_list: list,
                          feature_type: str = 'exon',
                          count_unit: str = 'transcript_id',
                          featureCounts_exec: str = 'featureCounts',
                          **kwargs):
        if self.ref_gff is None:
            echo(f'\33[31mError: Invalid reference genome annotation file "{self.ref_gff}".', err=True)
        featureCounts_exec = which(featureCounts_exec)
        out_path = f'{self.output_path}/04.expression'
        makedirs(out_path, exist_ok=True)
        bam_list.sort(key=natsort_key)
        bam_files = ' '.join(bam_list)
        cmd = f"{featureCounts_exec} " \
              f"-t {feature_type} " \
              f"-g {count_unit} " \
              f"-f -p -T {self.num_threads} " \
              f"-a {self.ref_gtf} " \
              f"-o {out_path}/featureCounts.xls " \
              f"{bam_files} "
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd
