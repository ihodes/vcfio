"""A Python library for reading and writing VCFs.
"""
from collections import OrderedDict

import vcf as pyvcf
import vcf.parser as vcfparser

import meta
import formats


__metaclass__ = EquivalentProperties


class VCF(object):
    def init(self):
        self.records = []
        self.spec = None

    def add_record(self, record):
        self.records.append(record)
        return self
    add = add_record

    @classmethod
    def from_text(cls, text):
        reader = pyvcf.Reader(l for l in text.split('\n'))
        vcf = cls()
        for record in reader:
            vcf.add_record(Record.from_vcf_record(record, vcf=vcf))
        vcf.spec = Spec.from_vcf_reader(vcf=vcf, reader=vcf)
        return vcf


class Spec(object):
    def __init__(self, vcf,
                 contigs=None, alts=None, infos=None, filters=None,
                 formats=None, sample_names=None, metadata=None):
        self.vcf = vcf
        self.contigs = contigs or OrderedDict()
        self.alts = alts or OrderedDict()
        self.infos = infos or OrderedDict()
        self.filters = filters or OrderedDict()
        self.formats = formats or OrderedDict()
        self.sample_names = sample_names or []
        self.metadata = metadata or OrderedDict()

    @classmethod
    def from_vcf_reader(cls, vcf, reader):
        return cls(
            vcf=vcf,
            contig=reader.contigs,
            alts=reader.alts,
            infos=reader.infos,
            formats=reader.formats,
            sample_names=reader.samples,
            metadata=reader.metadata
        )

    def add_contig(self, contig_id, length):
        self.contigs[contig_id] = vcfparser._Contig(id=contig_id, length=length)

    def add_alt(self, alt_id, description):
        return self.alts[alt_id] = vcfparser._Alt(
            id=alt_id, desc=description)

    def add_infos(self, info_id, number, type, description):
        return self.infos[info_id] = vcfparser._Info(
            id=info_id, num=number, type=type, desc=description)

    def add_filter(self, filter_id, description):
        return self.filters[filter_id] = vcfparser._Filter(
            id=filter_id, desc=description)

    def add_format(self, format_id, number, type, description):
        return self.formats[format_id] = vcfparser._Format(
            id=format_id, num=number, type=type, desc=description)

    def add_sample_name(self, name):
        self.sample_names.append(name)

    # def add_metadata(self, metadata_id, 


class Record(object):
    def __init__(self, vcf=None):
        self.vcf = vcf

    @meta.equivalent_property('chromosome', 'contig')
    def CHROM(self, value):
        return value

    @meta.equivalent_property('position')
    def POS(self, value):
        if value < 0:
            raise ValueError('position needs to be positive')
        return value

    @meta.equivalent_property('id')
    def ID(self, value):
        return value

    @meta.equivalent_property('reference')
    def REF(self, value):
        return value

    @meta.equivalent_property('alternates')
    def ALT(self, value):
        return value

    @meta.equivalent_property('filters')
    def FILTER(self, value):
        return value

    @meta.equivalent_property('info')
    def INFO(self, value):
        return value

    @meta.equivalent_property('format')
    def FORMAT(self, value):
        return value

    @meta.equivalent_property('genotypes')
    def calls(self, value):
        return value

    @classmethod
    def from_vcf_record(cls, vcfrecord, vcf=None):
        record = cls(vcf)
        attrs = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'FILTER', 'INFO', 'FORMAT']
        for attr in attrs:
            setattr(record, attr, getattr(vcfrecord, attr))
        record.calls = [Call.from_vcf_call(call, record=record)
                        for call in vcfrecord.samples]
        return record

    def __repr__(self):
        return 'VCFRecord(calls=[{}])'.format(call.name for call in calls)


class Call(object):
    def __init__(self, name, record, fields):
        self.name = name
        self.fields = fields
        self.record = record

    @classmethod
    def from_vcf_call(cls, call, record=None):
        return cls(call.sample, record, dict(call.data.__dict__))

    def __repr__(self):
        return "Call('{}')".format(self.name)


# class Foo(object):
#     def __init__(self):
#         self._bar = 1

#     @property
#     def bar(self):
#         print '..computed..'
#         return self._bar

#     @bar.setter
#     def bar(self, val):
#         self._bar = val
