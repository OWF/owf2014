#!/usr/bin/env python

import random

for i in range(0, 100):
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        if r + g + b > 500:
            print "#schedule .track%d { background-color: #%x%x%x; }\n" % (
                    i, r, g, b)
            break

