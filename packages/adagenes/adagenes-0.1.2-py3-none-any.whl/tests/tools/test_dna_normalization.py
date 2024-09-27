import unittest
import adagenes


class TestDNANormalization(unittest.TestCase):

    def test_pos_normalization(self):
        var = "chr7:140753336"
        var = adagenes.normalize_dna_identifier_position(var, add_refseq=False)
        self.assertEqual(var,"chr7:140753336","")

    def test_pos_normalization_rs(self):
        var = "chr7:g.140753336"
        var = adagenes.normalize_dna_identifier_position(var, add_refseq=False)
        self.assertEqual(var,"chr7:140753336","")

    def test_nc_normalization(self):
        var = "NC_000007.14:140753336A>T"
        var = adagenes.normalize_dna_identifier(var, add_refseq=False)
        self.assertEqual(var,"chr7:140753336A>T","")

    def test_nc_normalization_refseq(self):
        var = "NC_000007.14:g.140753336A>T"
        var = adagenes.normalize_dna_identifier(var, add_refseq=False)
        self.assertEqual(var,"chr7:140753336A>T","")

    def test_normalization(self):
        var = "chr7:140753336A>T"
        var = adagenes.normalize_dna_identifier(var, add_refseq=False)
        self.assertEqual(var,"chr7:140753336A>T","")

    def test_normalization_refseq(self):
        var = "chr7:g.140753336A>T"
        var = adagenes.normalize_dna_identifier(var, add_refseq=False)
        self.assertEqual(var,"chr7:140753336A>T","")