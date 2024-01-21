from tools.sort_words import sort_words

def test_order():
    sort_words('tests/res/order-dict-test.txt')
    expected = open('tests/res/order-dict-test-expected.txt', 'rt').read()
    result = open('tests/res/order-dict-test-sorted.txt', 'rt').read()
    assert result == expected # Words not ordered properly