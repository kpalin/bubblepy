# bubblepy
BubbleBabble class implementation for Python

Bubble Babble Binary Data Encoding - Python library

See http://bohwaz.net/archives/web/Bubble_Babble.html for details.

Original Copyright 2011 BohwaZ - http://bohwaz.net/
Copyleft 2015 europa - https://github.com/eur0pa

Based on :
- Bubble Babble spec: http://wiki.yak.net/589/Bubble_Babble_Encoding.txt
- Nitrxgen PHP script: http://www.nitrxgen.net/bubblebabble.php
- Bubble Babble encoder for Go: http://codereview.appspot.com/181122
- Bubble Babble class for PHP: https://github.com/bohwaz/bubblebabble

Use:

```python
  from BubblePy import BubbleBabble
  
  bb = BubbleBabble()
  
  print bb.encode('Pineapple')
  print bb.decode('xigak-nyryk-humil-bosek-sonax')
```
