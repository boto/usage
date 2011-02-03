# Copyright (c) 2009-2011 Mitch Garnaat http://garnaat.org/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

class Dimension(object):

    def __init__(self, service=None, operation=None, usage_type=None):
        self.service = service
        self.operation_name = operation
        self.usage_type = usage_type
        self.total = 0
        self.min = None
        self.max = None
        self.start = None
        self.end = None
        self.data = []

    def __repr__(self):
        return 'Dimension.%s.%s.%s' % (self.service, self.operation_name,
                                       self.usage_type)

    def add_usage(self, u):
        self.total += u.value
        if self.min == None or u.value < self.min:
            self.min = u.value
        if self.max == None or u.value > self.max:
            self.max = u.value
        if self.start == None or u.start < self.start:
            self.start = u.start
        if self.end == None or u.end > self.end:
            self.end = u.end
        self.data.append(u)

    def get_plot_data(self):
        l = []
        for u in self.data:
            l.append(u.value)
        return l

    
