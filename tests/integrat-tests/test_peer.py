import traceback

def test_link(node):

    assert node['core_1'].connectlist[0] == ['switch01', 8010, '127.0.0.1', 'sw']
    assert node['core_1'].connectlist[1] == ['switch02', 8011, '127.0.0.1', 'sw']
