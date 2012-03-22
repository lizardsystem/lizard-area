from lizard_area.sync_areas import properties_keys_to_lower

def test_a():
    assert len(properties_keys_to_lower({})) == 0

def test_b():
    orig_dict = {'gafsoort_krw': 'dont care'}
    assert orig_dict == properties_keys_to_lower(orig_dict)
    orig_dict = {'fsoort_krw': 'dont care'}
    assert {'gafsoort_krw': 'dont care'} == properties_keys_to_lower(orig_dict)
