import unittest
import artifical_variants

def get_helloworld():
    return 'hello world'

def test_get_helloworld():
    assert 'hello world' == get_helloworld()

def test_deletions():
    assert [{'ALT': 'A', 'REF': 'A', 'POS': 1111111, '#CHROM': 1}, {'ALT': 'A', 'REF': 'A', 'POS': 1111111, '#CHROM': 1}, {'ALT': 'A', 'REF': 'A', 'POS': 1111111, '#CHROM': 1}] == artifical_variants.get_deletions(1,1111111,'A')

def main():
    print(get_helloworld())

if __name__ == '__main__':
    main()
