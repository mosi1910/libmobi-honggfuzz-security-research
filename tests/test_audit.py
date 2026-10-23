"""Small self-tests; no target build or copyrighted e-book content required."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE/'scripts'))
from compare_lcov import compare, covered_identifiers
from summarize_campaigns import summarize
from derive_reproducer import derive

class TestAudit(unittest.TestCase):
    def test_lcov_parser(self):
        fixture='SF:libmobi/src/x.c\nFN:1,f\nFNDA:3,f\nDA:1,3\nDA:2,0\nBRDA:1,0,0,3\nBRDA:1,0,1,-\nend_of_record\n'
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.lcov'; a.write_text(fixture)
            r=covered_identifiers(a)
            self.assertEqual([len(r[k]) for k in ('lines','branches','functions')],[1,1,1])
            self.assertTrue(compare(a,a))

    def test_published_coverage_sets_equal(self):
        a=HERE/'data/coverage/original.lcov'
        b=HERE/'data/coverage/minimized.lcov'
        self.assertTrue(compare(a,b))

    def test_campaign_counts(self):
        records=summarize(HERE/'data/campaigns.csv')
        self.assertEqual(len(records),21)
        self.assertEqual(sum(r['iterations'] not in ('N/A','') for r in records),17)

    def test_reproducer_rejects_invalid_seed(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'fake.mobi';src.write_bytes(b'not a MOBI seed')
            with self.assertRaises(ValueError):derive(src,Path(d)/'out.mobi')
            self.assertFalse((Path(d)/'out.mobi').exists())

if __name__ == '__main__':
    unittest.main()
