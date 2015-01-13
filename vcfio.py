"""A Python library for reading and writing VCFs.
"""
import vcf as pyvcf
import copy

import meta
import formats


__metaclass__ = EquivalentProperties


class VCF(object):
    def __init__(self, text=None):
        self.records = [] # has many records
        self.spec = None
        if text:
            self._text = text
            # self._parse() # then run the VCF parser on it and make a VCF out of it

    def add_record(self, record):
        self.records.append(record)
        return self
    add = add_record


class Spec(object):
    pass


class Record(object):
    def __init__(self, vcf, sample_names=None):
        self.sample_names = sample_names
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

    def __repr__(self):
        return 'VCFRecord(calls=[{}])'.format(call.name for call in calls)


class Call(object):
    def __init__(self, name, record, fields):
        self.name = name
        self.fields = fields
        self.record = record

    def __repr__(self):
        return "Call('{}')".format(self.name)
