from hypothesis import given,example
from hypothesis.strategies import text,integers,characters
import pytest


@given(text(characters(max_codepoint=0xff)))
def test_decode_inverts_encode(s):
    from BubblePy import BubbleBabble
    bb = BubbleBabble()
    assert bb.decode(bb.encode(s)) == s


@given(integers(min_value=0))
@example(num=258)
@example(num=6580)
def test_encode(num):
    from BubblePy import BubbleBabble
    bb = BubbleBabble()
    assert isinstance(bb.encode(num),str)
   

@given(integers(min_value=0))
@example(num=258)
@example(num=6580)
def test_numeric_encoding_symmetry(num):
    from BubblePy import BubbleBabble
    bb = BubbleBabble()
    assert bb.decode(bb.encode(num),ret_int=True) == num
    


def test_given_encode():
    from BubblePy import BubbleBabble
    bb = BubbleBabble()

    tests = {
        '': 'xexax',
        'abcd': 'ximek-domek-gyxox',
        'asdf': 'ximel-finek-koxex',
        '0123456789': 'xesaf-casef-fytef-hutif-lovof-nixix',
        'Testing a sentence.': 'xihak-hysul-gapak-venyd-bumud-besek-heryl-gynek-vumuk-hyrox',
        '1234567890': 'xesef-disof-gytuf-katof-movif-baxux',
        'Pineapple': 'xigak-nyryk-humil-bosek-sonax',
    }

    for src, expected in list(tests.items()):
        res = bb.encode(src)
        assert res == expected
        res = bb.decode(res)
        assert res == src

def test_given_decode():
    from BubblePy import BubbleBabble
    bb = BubbleBabble()

    tests = {
        '': 'xexax',
        'abcd': 'ximek-domek-gyxox',
        'asdf': 'ximel-finek-koxex',
        '0123456789': 'xesaf-casef-fytef-hutif-lovof-nixix',
        'Testing a sentence.': 'xihak-hysul-gapak-venyd-bumud-besek-heryl-gynek-vumuk-hyrox',
        '1234567890': 'xesef-disof-gytuf-katof-movif-baxux',
        'Pineapple': 'xigak-nyryk-humil-bosek-sonax',
    }

    for src, expected in list(tests.items()):
        res = bb.decode(expected)
        assert res == src