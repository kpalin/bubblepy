#!/usr/bin/python2

"""
    Bubble Babble Binary Data Encoding - Python library

    See http://bohwaz.net/archives/web/Bubble_Babble.html for details.

    Original Copyright 2011 BohwaZ - http://bohwaz.net/
    Copyleft 2015 europa - https://github.com/eur0pa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Based on :
    - Bubble Babble spec: http://wiki.yak.net/589/Bubble_Babble_Encoding.txt
    - Nitrxgen PHP script: http://www.nitrxgen.net/bubblebabble.php
    - Bubble Babble encoder for Go: http://codereview.appspot.com/181122
    - Bubble Babble class for PHP: https://github.com/bohwaz/bubblebabble

    Use:

        from BubblePy import BubbleBabble

        bb = BubbleBabble()

        print bb.encode('Pineapple')
        print bb.decode('xigak-nyryk-humil-bosek-sonax')
"""


class BubbleBabble_Exception(Exception):
    """ exception handler for BubbleBabble class """
    pass


class BubbleBabble(object):
    """ encodes or decodes to and from bubblebabble """
    def __init__(self):
        super(BubbleBabble, self).__init__()
        self.vowels = 'aeiouy'
        self.consonants = 'bcdfghklmnprstvzx'

    def encode(self, src):
        out = 'x'
        c = 1

        for i in xrange(0, len(src) + 1, 2):
            if i >= len(src):
                out += self.vowels[c % 6] + self.consonants[16] + self.vowels[c / 6]
                break

            byte1 = ord(src[i])
            out += self.vowels[(((byte1 >> 6) & 3) + c) % 6]
            out += self.consonants[(byte1 >> 2) & 15]
            out += self.vowels[((byte1 & 3) + (c / 6)) % 6]

            if (i + 1) >= len(src):
                break

            byte2 = ord(src[i + 1])
            out += self.consonants[(byte2 >> 4) & 15]
            out += '-'
            out += self.consonants[byte2 & 15]

            c = (c * 5 + byte1 * 7 + byte2) % 36

        out += 'x'

        return out

    def decode(self, src):
        c = 1

        if src[0] is not 'x':
            raise BubbleBabble_Exception("corrupt string at offset 0: must begin with a 'x'")

        if src[-1] is not 'x':
            raise BubbleBabble_Exception("corrupt string at the last offset: must end with a 'x'")

        if len(src) != 5 and len(src) % 6 != 5:
            raise BubbleBabble_Exception("corrupt string: wrong length")

        src = src[1:-1]
        src = list(enumerate([src[x:x + 6] for x in range(0, len(src), 6)]))
        last_tuple = len(src) - 1
        out = ''

        for k, tup in src:
            pos = k * 6
            tup = self._decode_tuple(tup, pos)

            if k == last_tuple:
                if tup[1] == 16:
                    if tup[0] != c % 6:
                        raise BubbleBabble_Exception("corrupt string at offset %d (checksum)" % pos)

                    if tup[2] != int(c / 6):
                        raise BubbleBabble_Exception("corrupt string at offset %d (checksum)" % (pos + 2))
                else:
                    byte = self._decode_3way_byte(tup[0], tup[1], tup[2], pos, c)
                    out += chr(byte)
            else:
                    byte1 = self._decode_3way_byte(tup[0], tup[1], tup[2], pos, c)
                    byte2 = self._decode_2way_byte(tup[3], tup[5], pos)

                    out += chr(byte1)
                    out += chr(byte2)

                    c = (c * 5 + byte1 * 7 + byte2) % 36

        return out

    def _decode_tuple(self, src, pos):
        tupl = [self.vowels.index(src[0]),
                self.consonants.index(src[1]),
                self.vowels.index(src[2])]
        try:
            tupl.append(self.consonants.index(src[3]))
            tupl.append('-')
            tupl.append(self.consonants.index(src[5]))
        except:
            pass

        return tupl

    def _decode_2way_byte(self, a1, a2, offset):
        if a1 > 16:
            raise BubbleBabble_Exception("corrupt string at offset %d" % offset)

        if a2 > 16:
            raise BubbleBabble_Exception("corrupt string at offset %d" % (offset + 2))

        return (int(a1) << 4) | int(a2)

    def _decode_3way_byte(self, a1, a2, a3, offset, c):
        high2 = (a1 - (c % 6) + 6) % 6

        if high2 >= 4:
            raise BubbleBabble_Exception("corrupt string at offset %d" % offset)

        if int(a2) > 16:
            raise BubbleBabble_Exception("corrupt string at offset %d" % (offset + 1))

        mid4 = a2
        low2 = (a3 - (c / 6 % 6) + 6) % 6

        if low2 >= 4:
            raise BubbleBabble_Exception("corrupt string at offset %d" % (offset + 2))

        return high2 << 6 | mid4 << 2 | low2


if __name__ == '__main__':
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

    for src, expected in tests.items():
        res = bb.encode(src)
        assert res == expected
        res = bb.decode(res)
        assert res == src

    print 'tests passed'
