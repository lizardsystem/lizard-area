from lizard_area.sync_areas import Synchronizer

def test_a():
    synchronizer = Synchronizer()
    assert len(synchronizer.properties_keys_to_lower({})) == 0

def test_b():
    synchronizer = Synchronizer()
    orig_dict = {'gafsoort_krw': 'dont care'}
    assert orig_dict == synchronizer.properties_keys_to_lower(orig_dict)
    orig_dict = {'fsoort_krw': 'dont care'}
    assert {'gafsoort_krw': 'dont care'} == synchronizer.properties_keys_to_lower(orig_dict)
