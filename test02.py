#!/usr/bin/env python3
#-*- coding:utf-8 -*-

s1 = 72
s2 = 85
r = (s2 / s1 - 1) * 100
w = ((s2 - s1) / s1) * 100
print('小明的成绩提升了%.1f%%' % r)
print('小明的成绩提升了{0:.1f}%'.format(r))
print(f'小明的成绩提升了{r:.1f}%')
print('%.1f%%' % w)
