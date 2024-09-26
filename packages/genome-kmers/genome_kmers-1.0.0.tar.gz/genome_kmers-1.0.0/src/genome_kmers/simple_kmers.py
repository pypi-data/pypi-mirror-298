"""
This module contains classes implementing a simple implementation of the Kmers class, which uses
the simplest implementation of all major functionality. These classes will not perform well for
large, genome-level calculations, but are useful for unit testing and validation testing.

Implementation notes

Cases to handle:

- forward strand kmers only
- reverse complement strand kmers only
- both forward and reverse complement kmers

Kmer info needed to be tracked
- strand, chrom, seq_start_idx, seq_str, kmer_num, kmer_len

kmer sorting
- lexicographical
- canonical kmer

filtering

"""

from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Generator, Union

import numpy as np


def reverse_complement(seq):
    revcomp_map = {
        "A": "T",
        "C": "G",
        "G": "C",
        "T": "A",
        "R": "Y",
        "Y": "R",
        "S": "S",
        "W": "W",
        "K": "M",
        "M": "K",
        "B": "V",
        "D": "H",
        "H": "D",
        "V": "B",
        "N": "N",
    }
    revcomp_seq = "".join([revcomp_map[base] for base in seq[::-1]])
    return revcomp_seq


class SimpleSequenceCollection:
    """
    fwd_seqs = [seq_str_1, seq_str_2, ..]
    revcomp_seqs = [revcomp_seq_str_1, revcomp_seq_str_2, ..]
    record_names = [record_name_1, record_name_2, ..]
    """

    def __init__(
        self,
        seq_list: Union[list[tuple[str, str]]] = None,
        fasta_file_path: Union[Path, None] = None,
    ):
        if seq_list is None and fasta_file_path is None:
            raise ValueError(f"Either seq_list or fasta_file_path must be specified")
        if seq_list is not None and fasta_file_path is not None:
            raise ValueError(f"You can only specify one of seq_list and fasta_file_path")

        if seq_list is not None:
            self.initialize_with_seq_list(seq_list)
        else:
            self.initialize_with_fasta(fasta_file_path)

    def initialize_with_seq_list(self, seq_list):
        self.record_names = [record_name for record_name, _ in seq_list]
        self.fwd_seqs = [seq for _, seq in seq_list]
        self.revcomp_seqs = [reverse_complement(seq) for seq in self.fwd_seqs]

    def initialize_with_fasta(self, fasta_file_path):
        self.record_names = []
        self.fwd_seqs = []
        self.revcomp_seqs = []

        # read all lines of file
        with open(fasta_file_path, "r") as input_file:
            lines = input_file.readlines()

        # identify the start of all headers
        header_line_nums = []
        for n, line in enumerate(lines):
            if line.startswith(">"):
                record_name = line[1:].strip().split()[0]
                self.record_names.append(record_name)
                header_line_nums.append(n)

        # build all sequences
        # add a faux header line number at len(lines) to extract all sequences within the same loop
        header_line_nums.append(len(lines))
        for n in range(1, len(header_line_nums)):
            prev_header_line_num = header_line_nums[n - 1]
            header_line_num = header_line_nums[n]
            if header_line_num - prev_header_line_num <= 1:
                raise ValueError(f"fasta file is missing a sequence for a record")
            seq = "".join(
                [line.strip().upper() for line in lines[prev_header_line_num + 1 : header_line_num]]
            )
            self.fwd_seqs.append(seq)
            self.revcomp_seqs.append(reverse_complement(seq))

        if len(self.record_names) != len(self.fwd_seqs):
            msg = "Internal error initializing from fasta file."
            msg += " len(self.record_names) != len(self.fwd_seqs)"
            raise AssertionError(msg)

    def __str__(self):
        lines = []
        for record_name, fwd_seq, revcomp_seq in zip(
            self.record_names, self.fwd_seqs, self.revcomp_seqs
        ):
            lines.append(f"> {record_name}")
            lines.append(f"\t+ {fwd_seq}")
            lines.append(f"\t- {revcomp_seq}")
        return "\n".join(lines)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if self.fwd_seqs != other.fwd_seqs:
            return False
        if self.revcomp_seqs != other.revcomp_seqs:
            return False
        if self.record_names != other.record_names:
            return False
        return True


class SimpleKmer:
    """

    Description:
    - internally, all indices are zero-based
    - "*fwd_coord" means that indices are given in "forward strand coordinates"
    - "*local_coord" means that indices are gien in "local strand coordinates", which are relative to the 5' end of the strand
    - The start and end are defined on the local strand s.t. start_idx_local_coord <= end_idx_local_coord.
    - The start and end indices are inclusive

    Example:

    [chr1]
                                             start         end
                                               |            |
    seq_idx_fwd_coord:        0                17           30                               63
    seq_idx_local_coord:      0                17           30                               63
                              |                [  fwd_kmer  ]                                |
    forward              + 5' ATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGC 3'
    complement           - 3' TACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACG 5'
                                               [remk_pmocver]
                                               |            |
                                              end         start

    revcomp                5' GCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCAT 3'
                              |                                [revcomp_kmer]                |
    seq_idx_local_coord:      0                                33           46               63
    seq_idx_fwd_coord:        63                               30           17               0
                                                               |            |
                                                             start         end

        fwd_kmer
            # user provided
            strand: "+"
            seq_start_idx_local_coord: 17
            seq: TGCATGCATGCATG
            pre_seq_context: GCA
            post_seq_context: CAT
            record_num: 0
            record_name: "chr1"

            # calculated
            length: 14
            revcomp_seq: CATGCATGCATGCA
            revcomp_pre_seq_context: ATG
            revcomp_post_seq_context: TGC
            canonical_seq: CATGCATGCATGCA
            seq_start_idx_fwd_coord: 17
            seq_end_idx_local_coord: 30
            seq_end_idx_fwd_coord: 30

        revcomp_kmer
            # user provided
            strand: "-"
            seq_start_idx_local_coord: 33
            seq: CATGCATGCATGCA
            pre_seq_context: ATG
            post_seq_context: TGC
            record_num: 0
            record_name: "chr1"

            # calculated
            length: 14
            revcomp_seq: TGCATGCATGCATG
            revcomp_pre_seq_context: GCA
            revcomp_post_seq_context: CAT
            canonical_seq: CATGCATGCATGCA
            seq_start_idx_fwd_coord: 30
            seq_end_idx_local_coord: 46
            seq_end_idx_fwd_coord: 17
    """

    def __init__(
        self,
        strand: str,
        seq_start_idx_local_coord: int,
        seq: str,
        record_num: int,
        record_name: str,
        record_len: int,
        pre_seq_context: str = "",
        post_seq_context: str = "",
    ):
        # verify that arguments are valid
        if strand not in ("+", "-"):
            raise ValueError(f"strand '{strand}' is invalid")
        if seq_start_idx_local_coord < 0:
            raise ValueError(f"seq_start_idx_local_coord {seq_start_idx_local_coord} is invalid")
        if len(seq) == 0:
            raise ValueError(f"length of sequence ({len(seq)}) must be > 0")
        if record_num < 0:
            raise ValueError(f"record_num {record_num} is invalid")

        self.strand = strand
        self.seq_start_idx_local_coord = seq_start_idx_local_coord
        self.seq = seq
        self.record_num = record_num
        self.record_name = record_name
        self.record_len = record_len
        self.pre_seq_context = pre_seq_context
        self.post_seq_context = post_seq_context

        # calculate remaining class members
        self.length = len(seq)
        self.revcomp_seq = reverse_complement(seq)
        self.revcomp_pre_seq_context = reverse_complement(self.post_seq_context)
        self.revcomp_post_seq_context = reverse_complement(self.pre_seq_context)
        self.canonical_seq = self.seq if self.seq < self.revcomp_seq else self.revcomp_seq

        self.seq_start_idx_fwd_coord = self.get_fwd_coord(
            self.strand, self.seq_start_idx_local_coord, self.record_len
        )
        self.seq_end_idx_local_coord = self.seq_start_idx_local_coord + self.length - 1
        self.seq_end_idx_fwd_coord = self.get_fwd_coord(
            self.strand, self.seq_end_idx_local_coord, self.record_len
        )

    def get_key(self, kmer_comparison_type: str = "lexicographic"):
        if kmer_comparison_type == "lexicographic":
            return self.seq
        elif kmer_comparison_type == "canonical":
            return self.canonical_seq
        elif kmer_comparison_type == "location":
            # loc = f"{'+' if self.strand == 'forward' else '-'}{self.record_name}:{self.seq_start_idx_fwd_coord}"
            loc = f"{self.strand}{self.record_name}:{self.seq_start_idx_fwd_coord}"
            return loc
        else:
            raise ValueError(f"kmer_comparison_type '{kmer_comparison_type}' is invalid")

    @staticmethod
    def get_fwd_coord(strand, seq_idx_local_coord, record_len):
        if strand == "+":
            seq_idx_fwd_coord = seq_idx_local_coord
        elif strand == "-":
            seq_idx_fwd_coord = record_len - seq_idx_local_coord - 1
        else:
            raise ValueError(f"strand '{strand}' is invalid")
        return seq_idx_fwd_coord

    def __str__(self):
        return self.seq

    def __repr__(self):
        lines = []
        lines.append(f"seq: {self.seq}")
        lines.append(f"pre_seq_context: {self.pre_seq_context}")
        lines.append(f"post_seq_context: {self.post_seq_context}")
        lines.append(f"revcomp_seq: {self.revcomp_seq}")
        lines.append(f"revcomp_pre_seq_context: {self.revcomp_pre_seq_context}")
        lines.append(f"revcomp_post_seq_context: {self.revcomp_post_seq_context}")
        lines.append(f"canonical_seq: {self.canonical_seq}")
        lines.append(f"strand: {self.strand}")
        lines.append(f"record_num: {self.record_num}")
        lines.append(f"record_name: {self.record_name}")
        lines.append(f"length: {self.length}")
        lines.append(f"seq_start_idx_local_coord: {self.seq_start_idx_local_coord}")
        lines.append(f"seq_end_idx_local_coord: {self.seq_end_idx_local_coord}")
        lines.append(f"seq_start_idx_fwd_coord: {self.seq_start_idx_fwd_coord}")
        lines.append(f"seq_end_idx_fwd_coord: {self.seq_end_idx_fwd_coord}")
        return "\n".join(lines)


class SimpleKmers:
    """ """

    def __init__(
        self,
        seq_coll: SimpleSequenceCollection,
        kmer_len: Union[int, None] = None,
        pre_seq_context_len: int = 0,
        post_seq_context_len: int = 0,
    ) -> None:
        # verify that arguments are valid
        if kmer_len is not None and kmer_len < 1:
            raise ValueError(f"kmer_len {kmer_len} invalid")

        # initialize lists
        self.kmer_len = kmer_len
        self.fwd_kmers = self.initialize_kmers_by_strand(
            seq_coll.fwd_seqs,
            seq_coll.record_names,
            strand="+",
            pre_seq_context_len=pre_seq_context_len,
            post_seq_context_len=post_seq_context_len,
        )
        self.revcomp_kmers = self.initialize_kmers_by_strand(
            seq_coll.revcomp_seqs,
            seq_coll.record_names,
            strand="-",
            pre_seq_context_len=pre_seq_context_len,
            post_seq_context_len=post_seq_context_len,
        )
        self.fwd_and_revcomp_kmers = self.fwd_kmers[:] + self.revcomp_kmers[:]

        # set flag for whether Kmers has been sorted
        self._is_sorted = False
        # TODO: consider storing the kmer_comparison_type used for the sort and making it a
        # requirement that yielding is the same

    def initialize_kmers_by_strand(
        self,
        seqs: list[str],
        record_names: list[str],
        strand: str,
        pre_seq_context_len: int,
        post_seq_context_len: int,
    ) -> list[SimpleKmer]:

        kmers = []
        for record_num, (record_name, seq) in enumerate(zip(record_names, seqs)):
            record_len = len(seq)
            for idx_local_coord in range(len(seq)):

                # get kmer_seq and sequence context after the kmer
                if self.kmer_len is None:
                    kmer_seq = seq[idx_local_coord:]
                    post_seq_context = ""
                else:
                    kmer_seq = seq[idx_local_coord : idx_local_coord + self.kmer_len]
                    if len(kmer_seq) < self.kmer_len:
                        break

                    if idx_local_coord + self.kmer_len < len(seq):
                        start_idx = idx_local_coord + self.kmer_len
                        end_idx = start_idx + post_seq_context_len
                        post_seq_context = seq[start_idx:end_idx]
                    else:
                        post_seq_context = ""

                # get sequence context before the kmer
                start_idx = max(idx_local_coord - pre_seq_context_len, 0)
                pre_seq_context = seq[start_idx:idx_local_coord]

                # build Kmer object
                kmer = SimpleKmer(
                    strand=strand,
                    seq_start_idx_local_coord=idx_local_coord,
                    seq=kmer_seq,
                    record_num=record_num,
                    record_name=record_name,
                    record_len=record_len,
                    pre_seq_context=pre_seq_context,
                    post_seq_context=post_seq_context,
                )

                # append to list
                kmers.append(kmer)

        return kmers

    def get_kmers(
        self,
        strand: str,
        kmer_comparison_type: str = "lexicographic",
        min_group_size: int = 1,
        max_group_size: Union[int, None] = None,
        yield_first_n: Union[int, None] = None,
    ) -> Generator[tuple, None, None]:
        # verify strand is valid
        if strand == "+":
            kmers = self.fwd_kmers
        elif strand == "-":
            kmers = self.revcomp_kmers
        elif strand == "both":
            kmers = self.fwd_and_revcomp_kmers
        else:
            raise ValueError(f"strand '{strand}' is invalid")
        # TODO: verify other user parameters

        # if kmers have not been sorted, then ignore all parameters specified by the user except
        # strand
        if not self._is_sorted:
            kmer_comparison_type = "location"
            min_group_size = 1
            max_group_size = None
            yield_first_n = None

        # Build a helper dictionary that counts the number of kmers for each group
        kmer_group_size = Counter()
        for kmer in kmers:
            key = kmer.get_key(kmer_comparison_type)
            kmer_group_size[key] += 1

        # Walk through kmers yielding them if they pass all group filters
        num_already_yielded = Counter()
        for kmer in kmers:
            key = kmer.get_key(kmer_comparison_type)

            # get the group size
            group_size_total = kmer_group_size[key]

            # skip yielding if the group size is out of the allowed range
            if group_size_total < min_group_size:
                continue
            if max_group_size is not None and group_size_total > max_group_size:
                continue

            # skip yielding if we have already yielded "yield_first_n"
            if yield_first_n is not None and num_already_yielded[key] >= yield_first_n:
                continue

            # otherwise, yield the kmer
            if yield_first_n is None:
                group_size_yielded = group_size_total
            else:
                group_size_yielded = min(group_size_total, yield_first_n)
            yield kmer, group_size_yielded, group_size_total
            num_already_yielded[key] += 1

    def get_kmer_count(
        self,
        strand: str,
        kmer_comparison_type: str = "lexicographic",
        min_group_size: int = 1,
        max_group_size: Union[int, None] = None,
    ) -> int:
        kmer_generator = self.get_kmers(
            strand, kmer_comparison_type, min_group_size, max_group_size, yield_first_n=1
        )
        total_kmer_count = 0
        for kmer, group_size_yielded, group_size_total in kmer_generator:
            total_kmer_count += group_size_total
        return total_kmer_count

    def get_kmer_group_counts(
        self,
        strand: str,
        kmer_comparison_type: str = "lexicographic",
        min_group_size: int = 1,
        max_group_size: Union[int, None] = None,
        max_counts_bin: int = 1000000,
    ) -> tuple[np.ndarray, int]:
        kmer_generator = self.get_kmers(
            strand, kmer_comparison_type, min_group_size, max_group_size, yield_first_n=1
        )
        total_kmer_count = 0
        counts_by_group_size = np.zeros((max_counts_bin + 1,))
        for kmer, group_size_yielded, group_size_total in kmer_generator:
            total_kmer_count += group_size_total
            counts_by_group_size[group_size_total] += 1
        return counts_by_group_size, total_kmer_count

    def sort(self, kmer_comparison_type: str = "lexicographic"):
        self.fwd_kmers.sort(key=lambda kmer: kmer.get_key(kmer_comparison_type))
        self.revcomp_kmers.sort(key=lambda kmer: kmer.get_key(kmer_comparison_type))
        self.fwd_and_revcomp_kmers.sort(key=lambda kmer: kmer.get_key(kmer_comparison_type))
        self._is_sorted = True

    def filter(self, filters=[]):
        for kmers in (self.fwd_kmers, self.revcomp_kmers, self.fwd_and_revcomp_kmers):
            # build a list of indices for passing kmers
            passing_kmer_indices = set()
            for n, kmer in enumerate(kmers):
                kmer_passes_all_filters = True
                for filter in filters:
                    if not filter.does_kmer_pass(kmer):
                        kmer_passes_all_filters = False
                        break
                if kmer_passes_all_filters:
                    passing_kmer_indices.add(n)

            # reset the list of kmers to only include those that have passed all filters
            kmers = [kmer for n, kmer in enumerate(kmers) if n in passing_kmer_indices]


class MaxHomopolymerFilter:
    def __init__(self, max_homopolymer_size: int):
        self.max_homopolymer_size = max_homopolymer_size

    @staticmethod
    def get_length_of_longest_homopolymer(kmer: SimpleKmer) -> int:
        if kmer.length < 1:
            raise ValueError(f"kmer.length ({kmer.length}) is < 1")

        len_longest_homopolymer = 1
        len_current_homopolymer = 1
        for i in range(1, kmer.length):
            prev_base = kmer.seq[i - 1]
            base = kmer.seq[i]
            if base == prev_base:
                len_current_homopolymer += 1
            else:
                if len_current_homopolymer > len_longest_homopolymer:
                    len_longest_homopolymer = len_current_homopolymer
                len_current_homopolymer = 1

        # Check to see if the last homopolymer exceeds the longest
        if len_current_homopolymer > len_longest_homopolymer:
            len_longest_homopolymer = len_current_homopolymer

        return len_longest_homopolymer

    def does_kmer_pass(self, kmer: SimpleKmer) -> bool:
        if self.get_length_of_longest_homopolymer(kmer) <= self.max_homopolymer_size:
            return True
        return False


class GCFilter:
    def __init__(self, min_allowed_gc_frac: float, max_allowed_gc_frac: float):
        self.min_allowed_gc_frac = min_allowed_gc_frac
        self.max_allowed_gc_frac = max_allowed_gc_frac

    @staticmethod
    def get_gc_frac(kmer: SimpleKmer) -> float:
        # calculate the fraction GC content
        counter = Counter(kmer.seq)
        if set(counter.keys()) - {"A", "T", "G", "C"} != set():
            raise ValueError(f"There were bases besides A, T, G, C in the kmer")
        gc_frac = (counter["G"] + counter["C"]) / len(kmer.length)
        return gc_frac

    def does_kmer_pass(self, kmer: SimpleKmer) -> bool:
        gc_frac = self.get_gc_frac(kmer)
        if self.min_allowed_gc_frac <= gc_frac <= self.max_allowed_gc_frac:
            return True
        return False


class NoAmbiguousBasesFilter:
    def __init__(self):
        pass

    def does_kmer_pass(self, kmer: SimpleKmer) -> bool:
        bases = set(kmer.seq)
        if bases - {"A", "T", "G", "C"} != set():
            return False
        return True


class CrisprNggPamFilter:
    def __init__(self):
        pass

    def does_kmer_pass(self, kmer: SimpleKmer) -> bool:
        if kmer.length != 20:
            raise ValueError(f"kmer.length ({kmer.length}) != 20")

        if len(kmer.post_seq_context) >= 3 and kmer.post_seq_context[1:3] == "GG":
            return True
        return False
