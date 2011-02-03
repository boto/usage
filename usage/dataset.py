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

import xml.sax
import usage
import dimension

class XmlHandler(xml.sax.ContentHandler):

    def __init__(self, dataset):
        self.dataset = dataset
        self.service_name = None
        self.operation_name = None
        self.usage_type = None
        self.current_usage = None
        self.current_text = ''

    def startElement(self, name, attrs):
        self.current_text = ''
        if name == 'OperationUsage':
            self.current_usage = usage.Usage()

    def endElement(self, name):
        value = self.current_text
        self.current_text = ''
        if name == 'ServiceName':
            self.service_name = value
        elif name == 'OperationName':
            self.operation_name = value
        elif name == 'UsageType':
            self.usage_type = value
        elif name == 'StartTime':
            self.current_usage.start = value
        elif name == 'EndTime':
            self.current_usage.end = value
        elif name == 'UsageValue':
            self.current_usage.value = value
        elif name == 'OperationUsage':
            self.dataset.add_usage(self.service_name, self.operation_name,
                                   self.usage_type, self.current_usage)
            self.current_usage = None
        elif name == 'ServiceUsage':
            pass
        else:
            print 'Unknown Attribute: %s' % name

    def characters(self, content):
        self.current_text += content
        
class DataSet(dict):

    def __init__(self, key=None):
        self.current_usage = None
        if key:
            self.load(key)

    def add_usage(self, service_name, operation_name, usage_type, usage):
        key = '%s.%s.%s' % (service_name, operation_name, usage_type)
        if key not in self:
            self[key] = dimension.Dimension(service_name, operation_name, usage_type)
        self[key].add_usage(usage)
        
    def load(self, path):
        h = XmlHandler(self)
        xml.sax.parse(path, h)

    
