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
import dateutil.parser
import StringIO

class EBSRequests(object):

    def __init__(self, dataset):
        self.reads = dataset['AmazonEC2.EBS:IO-Read.EBS:VolumeIOUsage']
        self.writes = dataset['AmazonEC2.EBS:IO-Write.EBS:VolumeIOUsage']

    def total(self):
        return self.reads.total + self.writes.total

    def cost(self):
        return self.total() / 1000000 * 0.10

class EBSSnapShotPuts(object):
    
    def __init__(self, dataset):
        self.puts = dataset['AmazonEC2.CreateSnapshot.EBS:SnapshotPutUsage']

    def total(self):
        return self.puts.total

    def cost(self):
        return self.total() / 1000 * 0.01

class EBSSnapShotStorage(object):
    
    def __init__(self, dataset):
        self.storage = dataset['AmazonEC2.CreateSnapshot.EBS:SnapshotUsage']

    def total(self):
        return self.storage.total

    def cost(self):
        return self.total() / 1000000000 * 0.15

class EBSReports(object):

    def __init__(self, dataset):
        self.requests = EBSRequests(dataset)
        self.snapshot_puts = EBSSnapShotPuts(dataset)
        self.snapshot_storage = EBSSnapShotStorage(dataset)

    def report(self):
        print 'EBS Reports'
        print '-----------'
        print '%d I/O Requests     = %f' % (self.requests.total(),
                                            self.requests.cost())
        print '%d SnapShot Puts    = %f' % (self.snapshot_puts.total(),
                                            self.snapshot_puts.cost())
        print '%d SnapShot Storage = %f' % (self.snapshot_storage.total(),
                                            self.snapshot_storage.cost())


    def bandwidth_report(self):
        d1 = self['AmazonEC2.ElasticIP-In.DataTransfer-Regional-Bytes']
        d2 = self['AmazonEC2.ElasticIP-Out.DataTransfer-Regional-Bytes']
        fp = StringIO.StringIO()
        fp.write(" <script type='text/javascript'>\n")
        fp.write("    google.load('visualization', '1', {'packages':['annotatedtimeline']});\n")
        fp.write("    google.setOnLoadCallback(drawChart);\n")
        fp.write("      function drawChart() {\n")
        fp.write("        var data = new google.visualization.DataTable();\n")
        fp.write("        data.addColumn('datetime', 'Date');\n")
        fp.write("        data.addColumn('number', 'Regional Transfer In');\n")
        fp.write("        data.addColumn('string', 'title1');\n")
        fp.write("        data.addColumn('string', 'text1');\n")
        fp.write("        data.addColumn('number', 'Regional Transfer Out');\n")
        fp.write("        data.addColumn('string', 'title2');\n")
        fp.write("        data.addColumn('string', 'text2');\n")
        fp.write("        data.addRows([\n")
        for i in range(0, len(d2.data)):
            u1 = d1.data[i]
            u2 = d2.data[i]
            fp.write("          [new Date(")
            fp.write("%d, %d, %d, %d, %d, %d)," % (u1.end.year, u1.end.month, u1.end.day,
                                                 u1.end.hour, u1.end.minute, u1.end.second))
            fp.write("%d, undefined, undefined, " % u1.value)
            fp.write("%d, undefined, undefined],\n " % u2.value)
        fp.write("        ]);\n")
        fp.write("        var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('chart_div'));\n")
        fp.write("        chart.draw(data, {displayAnnotations: true});\n")
        fp.write("      }\n")
        fp.write("    </script>\n")
        return fp.getvalue()

    def ebs_report(self):
        d1 = self['AmazonEC2.EBS:IO-Write.EBS:VolumeIOUsage']
        d2 = self['AmazonEC2.EBS:IO-Read.EBS:VolumeIOUsage']
        fp = StringIO.StringIO()
        fp.write(" <script type='text/javascript'>\n")
        fp.write("    google.load('visualization', '1', {'packages':['annotatedtimeline']});\n")
        fp.write("    google.setOnLoadCallback(drawChart);\n")
        fp.write("      function drawChart() {\n")
        fp.write("        var data = new google.visualization.DataTable();\n")
        fp.write("        data.addColumn('datetime', 'Date');\n")
        fp.write("        data.addColumn('number', 'EBS I/O Write');\n")
        fp.write("        data.addColumn('string', 'title1');\n")
        fp.write("        data.addColumn('string', 'text1');\n")
        fp.write("        data.addColumn('number', 'EBS I/O Read');\n")
        fp.write("        data.addColumn('string', 'title2');\n")
        fp.write("        data.addColumn('string', 'text2');\n")
        fp.write("        data.addRows([\n")
        for i in range(0, len(d2.data)):
            u1 = d1.data[i]
            u2 = d2.data[i]
            fp.write("          [new Date(")
            fp.write("%d, %d, %d, %d, %d, %d)," % (u1.end.year, u1.end.month, u1.end.day,
                                                 u1.end.hour, u1.end.minute, u1.end.second))
            fp.write("%d, undefined, undefined, " % u1.value)
            fp.write("%d, undefined, undefined],\n " % u2.value)
        fp.write("        ]);\n")
        fp.write("        var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('chart_div'));\n")
        fp.write("        chart.draw(data, {displayAnnotations: true});\n")
        fp.write("      }\n")
        fp.write("    </script>\n")
        return fp.getvalue()
    
