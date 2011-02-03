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

import dateutil.parser

class Usage(object):

    def __init__(self):
        self._start = None
        self._start_string = None
        self._end = None
        self._end_string = None
        self._value = None
        self._value_string = None

    def get_start(self):
        return self._start

    def set_start(self, date_string):
        self._start_string = date_string
        self._start = dateutil.parser.parse(date_string)

    start = property(get_start, set_start, None,
                      'The start date for this Usage')

    def get_end(self):
        return self._end

    def set_end(self, date_string):
        self._end_string = date_string
        self._end = dateutil.parser.parse(date_string)

    end = property(get_end, set_end, None,
                   'The end date for this Usage')

    def get_value(self):
        return self._value

    def set_value(self, value_string):
        self._value_string = value_string
        self._value = int(value_string)

    value = property(get_value, set_value, None,
                   'The usage value for this Usage')

        
    
