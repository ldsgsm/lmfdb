# -*- coding: utf-8 -*-

from lmfdb.tests import LmfdbTest
from lmfdb import db

class SatoTateGroupTest(LmfdbTest):

    # All tests should pass
    #
    def test_main(self):
        L = self.tc.get('/SatoTateGroup/')
        assert 'Browse' in L.get_data(as_text=True) and 'U(1)' in L.get_data(as_text=True) and 'U(1)_2' in L.get_data(as_text=True) and 'SU(2)' in L.get_data(as_text=True) and 'Rational' in L.get_data(as_text=True)
        
    def test_by_label(self):
        L = self.tc.get('/SatoTateGroup/?label=1.4.A.1.1a', follow_redirects=True)
        assert 'USp(4)' in L.get_data(as_text=True) and '223412' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?label=1.4.USp(4)', follow_redirects=True)
        assert '1.4.A.1.1a' in L.get_data(as_text=True) and '223412' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?label=1.2.N(U(1))', follow_redirects=True)
        assert '1.2.B.2.1a' in L.get_data(as_text=True) and '462' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?label=0.1.37', follow_redirects=True)
        assert '0.1.37' in L.get_data(as_text=True) and 'mu(185)' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?label=0.1.mu(37)', follow_redirects=True)
        assert '0.1.37' in L.get_data(as_text=True) and 'mu(185)' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?label=0.1.mu(100000000000000000001)', follow_redirects=True)
        assert 'too large' in L.get_data(as_text=True)

    def test_direct_access(self):
        L = self.tc.get('/SatoTateGroup/1.4.G_{3,3}', follow_redirects=True)
        assert '1.4.B.1.1a' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/G_{3,3}', follow_redirects=True)
        assert '1.4.B.1.1a' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/1.4.SU(2)xSU(2)', follow_redirects=True)
        assert '1.4.B.1.1a' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/SU(2)XSU(2)', follow_redirects=True)
        assert '1.4.B.1.1a' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/banana', follow_redirects=True)
        assert 'The database currently contains' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/1.4.B.1.1a')
        assert 'SU(2)xSU(2)' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/0.1.mu(37)', follow_redirects=True)
        assert '0.1.37' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/0.1.37')
        assert 'mu(37)' in L.get_data(as_text=True)

    def test_browse(self):
        L = self.tc.get('/SatoTateGroup/?identity_component=U(1)')
        assert 'both matches' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?weight=1&degree=4&include_irrational=yes&components=48')
        assert 'unique match' in L.get_data(as_text=True)
        L = self.tc.get('SatoTateGroup/?components=48&include_irrational=yes')
        assert '27 matches' in L.get_data(as_text=True)
        L = self.tc.get('SatoTateGroup/?degree=1&start=1000&count=25&include_irrational=yes')
        assert 'matches 1001-1025' in L.get_data(as_text=True)
        L = self.tc.get('SatoTateGroup/?degree=1')
        assert 'both matches' in L.get_data(as_text=True)
        L = self.tc.get('SatoTateGroup/?count=47')
        assert '1-47' in L.get_data(as_text=True)

    def test_moments(self):
        L = self.tc.get('/SatoTateGroup/1.4.B.1.1a')
        assert '187348' in L.get_data(as_text=True)

    def test_subgroups(self):
        L = self.tc.get('/SatoTateGroup/1.4.F.6.1a')
        assert 'C_2' in L.get_data(as_text=True) and 'C_3' in L.get_data(as_text=True)
        assert 'D_{6,1}' in L.get_data(as_text=True) and 'D_6' in L.get_data(as_text=True) and 'J(D_3)' in L.get_data(as_text=True) and 'O' in L.get_data(as_text=True)

    def test_event_probabilities(self):
        L = self.tc.get('/SatoTateGroup/1.4.F.48.48a')
        assert '23' in L.get_data(as_text=True)

    def test_completeness(self):
        import sys
        L = self.tc.get('/SatoTateGroup/?weight=1&degree=2')
        assert '3 matches' in L.get_data(as_text=True)
        data = list(db.gps_st.search({'weight':int(1),'degree':int(2)}, projection='label'))
        assert len(data) == 3
        print("")
        for label in data:
            sys.stdout.write("{}...".format(label))
            sys.stdout.flush()
            L = self.tc.get('/SatoTateGroup/' + label)
            assert label in L.get_data(as_text=True) and 'Moment sequences' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?weight=1&degree=4')
        assert 'of 52' in L.get_data(as_text=True)
        data = list(db.gps_st.search({'weight':int(1),'degree':int(4)}, projection='label'))
        assert len(data) == 52

        for label in data:
            sys.stdout.write("{}...".format(label))
            sys.stdout.flush()
            L = self.tc.get('/SatoTateGroup/' + label)
            assert label in L.get_data(as_text=True) and 'Moment sequences' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?components=999999999&include_irrational=yes')
        assert 'unique match' in L.get_data(as_text=True) and 'mu(999999999)' in L.get_data(as_text=True)

    def test_trace_zero_density(self):
        L = self.tc.get('/SatoTateGroup/?trace_zero_density=1')
        assert 'No matches' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?trace_zero_density=1/4')
        assert '1.4.E.4.1a' in L.get_data(as_text=True)
        L = self.tc.get('/SatoTateGroup/?trace_zero_density=19/24')
        assert '1.4.F.24.14a' in L.get_data(as_text=True)

    def test_favourites(self):
        for label in [ '1.2.1.2.1a','1.2.3.1.1a', '1.4.1.12.4d', '1.4.3.6.2a', '1.4.6.1.1a', '1.4.10.1.1a' ]:
            L = self.tc.get('/SatoTateGroup/'+label, follow_redirects=True)
            assert "Moment sequences" in L.get_data(as_text=True)
        for label in [ '1.2.B.2.1a','1.2.A.1.1a', '1.4.F.12.4d', '1.4.E.6.2a', '1.4.B.1.1a', '1.4.A.1.1a' ]:
            L = self.tc.get('/SatoTateGroup/'+label)
            assert "Moment sequences" in L.get_data(as_text=True)

