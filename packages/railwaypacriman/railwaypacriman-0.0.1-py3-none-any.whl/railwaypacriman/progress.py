#! /usr/bin/env python3

## module Progress, to show progress
## Last-modified:2024/09/27 23:51:07.
## Author: Ippei KISHIDA

import graphviz
import math
import unittest
import sys
from railwaypacriman.line import *
#import railwaypacriman.line
import railwaypacriman.logger as lggr

nc = '#000000ff' #nc: node color with alpha channel
fc = '#f0f0f0ff' #fc: fill color for node with alpha channel
fontname = 'Noto Sans CJK JP' #fontname: font name
fs = '7' #fs: font size. String is given to node of graphviz

def linefeed_square(string):
    width = math.ceil( math.sqrt(len(string))) # width == height
    ary = []
    for i in range(0, width):
        if (width * (i+1)) > len(string):
            end = len(string)
        else:
            end = (width * (i+1)) 
        ary.append( string[(width * i) : end])
    return "\n".join(ary).strip()

class Progress:
    def __init__(self):
        self.lines = {}

    def __str__(self):
        result = '{'
        for key, val in self.lines.items():
            result += str(key) + ':' + str(val) + ','

        result += '}'
        return result

    def edge_style(self, direction, activity):
        options = { 'arrowsize': '0.5'}
        if direction == 'both' and activity == 'run':
            options.update({'color': '#000000', 'dir': 'both', 'penwidth': '2'})
            return options
        r = "00"
        g = "00"
        b = "00"
        if activity == "bike":
            g = 'd0'

        if direction == "up":
            r = 'ff'
            options['dir'] = 'back'
        elif direction == "down":
            b = 'ff'
            options['dir'] = 'forward'
        else:
            r = "d0"
            g = "d0"
            b = "d0"
            options['arrowhead'] = 'none'

        options['color'] = '#' + r + g + b
        return options

    def proceed(self, date, line_cd, from_station_cd, to_station_cd, activity, inout):
        ## 初めてのアクセスで Line インスタンス作成
        if not self.lines.get(line_cd):
            #self.lines[line_cd] = Line(line_cd)
            self.lines[line_cd] = Line(line_cd)

        try:
            from_idx = self.lines[line_cd].st_cds.index(from_station_cd)
        except ValueError: 
            print("Not found {} in {}".format(from_station_cd, line_cd))
            return

        try:
            to_idx   = self.lines[line_cd].st_cds.index(to_station_cd)
        except ValueError: 
            print("Not found {} in {}".format(to_station_cd, line_cd))
            return

        l = self.lines[line_cd]
        l.tread(from_idx, to_idx, activity, inout)

    # num_char: number of characters for station name. 0 means unlimited
    def draw_graph(self, outfile, tgt_line_cds, geological, num_letter=9999):
        ## 描画対象の路線を整理
        #print(tgt_line_cds); sys.exit()
        for i in tgt_line_cds:
            if not i in list(self.lines.keys()):
                #print(i)
                #print(Line(i))
                self.lines[i] = Line(i)
            #try:
            #    if not i in list(self.lines.keys()):
            #        self.lines[i] = Line(i)
            #except IndexError:
            #    print("Not found in data: " + str(i))
            #    continue
        #print(self.lines); sys.exit()

        ## 描画順となる会社順に整理
        companies = defaultdict(list)
        for i in tgt_line_cds:
            #print(companies)
            #print([self.lines[i]])
            companies[self.lines[i].company_cd].append(i)
        tgt_line_cds = []
        for c in sorted(companies.keys()):
            for i in sorted(companies[c]):
                tgt_line_cds.append(i)

        #print(outfile, tgt_line_cds, geological); sys.exit()
        if geological:
            g = graphviz.Digraph(engine='neato')
            lo_list = []
            la_list = []
            for line_cd in tgt_line_cds:
                for scd in sd.loc[sd['line_cd'] == line_cd, 'station_cd']:
                    lo_list.append(float(sd.loc[sd['station_cd'] == scd, 'lon'].values[0]))
                    la_list.append(float(sd.loc[sd['station_cd'] == scd, 'lat'].values[0]))
            lo_min = min(lo_list) #lo_max: longitude max 
            lo_max = max(lo_list) #lo_min: longitude min 
            la_min = min(la_list) #la_max: latitude max  
            la_max = max(la_list) #la_min: latitude min  
        else:
            g = graphviz.Digraph()
            g.attr(ranksep='0.5') #0.5 が default

        #for line_cd in sorted(self.lines.keys()):
        for line_cd in tgt_line_cds:
            line = self.lines[line_cd]
            if (not tgt_line_cds) or (not line.line_cd in tgt_line_cds):
                continue

            lggr.log("## " + line.line_name)
            with g.subgraph(name = "cluster_" + line.line_name) as c:
                options = {'color': 'black', 'penwidth': '0'}
                if not geological:
                    options['label'] = linefeed_square(line.line_name)
                c.attr(** options)
                lggr.log("### nodes")
                for i in range(0, len(line.st_cds)):
                    scd = int(line.st_cds[i])
                    args = {
                            'name': str(line.line_cd) + '-' + str(i), #nn: node name
                            'label': linefeed_square(line.st_names[i][:num_letter]), #nl: node label
                            'style': 'filled',
                            'color': nc,
                            'margin': '0.0,0.0',
                            'fontsize': fs,
                            'width': '0.3',
                            'height': '0.3',
                            'fillcolor': fc}
                    if geological:
                        lo = float(sd.loc[sd['station_cd'] == scd, 'lon'].values[0])
                        la = float(sd.loc[sd['station_cd'] == scd, 'lat'].values[0])
                        mb = 20 # base multiplier, フォントと図のサイズ調整のための倍率
                        ml = math.cos(35.0/360.0 * (2*math.pi)) # 経度:緯度の倍率。緯度35度を仮定。

                        multiply =  mb / (lo_max - lo_min)
                        x = multiply * (lo - lo_min) * ml
                        y = multiply * (la - la_min)
                        args['pos'] = str(x) + ',' + str(y) + '!'
                    if fontname:
                        args['fontname'] = fontname
                    if len(args['label']) <= 1:
                        args['shape'] = 'circle'
                        args['width'] = '0.1'
                        args['height'] = '0.1'
                        g.attr(ranksep='0.3') #0.5 が default
                    c.node(** args)

                ##fscd: from station_cd
                ##tscd: to station_cd
                for key, value in line.joins.items():
                    (fscd, tscd) = key
                    fn = str(line.line_cd) + '-' + str(fscd) # fn: from_node
                    tn = str(line.line_cd) + '-' + str(tscd) # tn: to_node
                    tgt_edges = value.unique_arrows()
                    if not tgt_edges: # empty
                        tgt_edges = [('', '')] ## for just connection
                    elif (('up', 'run') in tgt_edges) and (('down', 'run') in tgt_edges):
                        tgt_edges = [('both', 'run')] ## for just connection

                    for edge in tgt_edges:
                        options = self.edge_style(* edge)
                        c.edge(fn, tn, **options)

        g.attr(dpi='72')
        g.render(outfile, format='png')

if __name__=="__main__":
    class UnitTest(unittest.TestCase):
        def test_add(self):
            expected = "abc\ndef\ng"
            actual = linefeed_square("abcdefg")
            self.assertEqual(expected, actual)

            expected = "abcd\nefgh\nijkl\nm"
            actual = linefeed_square("abcdefghijklm")
            self.assertEqual(expected, actual)

            expected = "abcd\nefgh\nijkl\nmnop"
            actual = linefeed_square("abcdefghijklmnop")
            self.assertEqual(expected, actual)

            expected = "abcde\nfghij\nklmno\npq"
            actual = linefeed_square("abcdefghijklmnopq")
            self.assertEqual(expected, actual)

        def test_arrowcolor(self):
            p0 = Progress()

            expected = {'color': "#0000ff", 'dir': 'forward'}
            actual = p0.edge_style('down', 'run')
            self.assertEqual(expected, actual)

            expected = {'color': "#00d0ff", 'dir': 'forward'}
            actual = p0.edge_style('down', 'bike')
            self.assertEqual(expected, actual)

            expected = {'color': "#ff0000", 'dir': 'back'}
            actual = p0.edge_style('up', 'run')
            self.assertEqual(expected, actual)

            expected = {'color': "#ffd000", 'dir': 'back'}
            actual = p0.edge_style('up', 'bike')
            self.assertEqual(expected, actual)

            expected = {'color': "#d0d0d0", 'arrowhead': 'none'}
            actual = p0.edge_style('', '')
            self.assertEqual(expected, actual)

        def test_str(self):
            p0 = Progress()

            actual = '{}'
            expected = p0.__str__()
            self.assertEqual(expected, actual)

            p0.proceed('2024-08-19', 34007, 3400704, 3400701, "run", False)
            #print(p0)
            actual = "{34007:阪急箕面線,34007,[3400701, 3400702, 3400703, 3400704],['石橋阪大前', '桜井', '牧落', '箕面'],{joins:(0, 1):[['up', 'run']],(1, 2):[['up', 'run']],(2, 3):[['up', 'run']],,},}"
            expected = p0.__str__()
            self.assertEqual(expected, actual)

            pass

        def test_proceed1(self): ##nobori
            p0 = Progress()

            actual = len(p0.lines)
            expected = 0
            self.assertEqual(expected, actual)

            p0.proceed('2024-08-19', 34007, 3400704, 3400701, "run", False)
            actual = len(p0.lines)
            expected = 1
            self.assertEqual(expected, actual)

            actual = list(p0.lines.keys())
            expected = [34007]
            self.assertEqual(expected, actual)

            actual = p0.lines[34007].name
            expected = '阪急箕面線'
            self.assertEqual(expected, actual)

            actual = len(p0.lines[34007].joins)
            expected = 3
            self.assertEqual(expected, actual)

            expected = [['up', 'run']]
            actual = p0.lines[34007].joins[(0,1)].records
            self.assertEqual(expected, actual)

            expected = [['up', 'run']]
            actual = p0.lines[34007].joins[(1,2)].records
            self.assertEqual(expected, actual)

            expected = [['up', 'run']]
            actual = p0.lines[34007].joins[(2,3)].records
            self.assertEqual(expected, actual)

        def test_proceed2(self): ##kudari
            p0 = Progress()

            actual = len(p0.lines)
            expected = 0
            self.assertEqual(expected, actual)

            p0.proceed('2024-08-19', 34007, 3400701, 3400704, "run", False)
            actual = p0.lines[34007].joins

            expected = [['down', 'run']]
            actual = p0.lines[34007].joins[(0,1)].records
            self.assertEqual(expected, actual)

            expected = [['down', 'run']]
            actual = p0.lines[34007].joins[(1,2)].records
            self.assertEqual(expected, actual)

            expected = [['down', 'run']]
            actual = p0.lines[34007].joins[(2,3)].records
            self.assertEqual(expected, actual)

        def test_proceed3(self): ##bike
            p0 = Progress()

            actual = len(p0.lines)
            expected = 0
            self.assertEqual(expected, actual)

            p0.proceed('2024-08-19', 34007, 3400704, 3400701, "bike", False)

            expected = [['up', 'bike']]
            actual = p0.lines[34007].joins[(0,1)].records
            self.assertEqual(expected, actual)

            expected = [['up', 'bike']]
            actual = p0.lines[34007].joins[(1,2)].records
            self.assertEqual(expected, actual)

            expected = [['up', 'bike']]
            actual = p0.lines[34007].joins[(2,3)].records
            self.assertEqual(expected, actual)

        def test_proceed4(self): ##loop, out
            p0 = Progress()

            actual = len(p0.lines)
            expected = 0
            self.assertEqual(expected, actual)

            p0.proceed('2024-08-19', 11623, 1162319, 1162302 , "run", 'out') #寺田町→天王寺→新今宮

            expected = [['down', 'run']]
            actual = p0.lines[11623].joins[(0,1)].records
            self.assertEqual(expected, actual)

            expected = []
            actual = p0.lines[11623].joins[(1,2)].records
            self.assertEqual(expected, actual)

            expected = []
            actual = p0.lines[11623].joins[(17,18)].records
            self.assertEqual(expected, actual)

            expected = [['down', 'run']]
            actual = p0.lines[11623].joins[(18,0)].records
            self.assertEqual(expected, actual)

        def test_proceed5(self): ##loop, in
            p0 = Progress()

            actual = len(p0.lines)
            expected = 0
            self.assertEqual(expected, actual)

            p0.proceed('2024-08-19', 11623, 1162302 , 1162319, "run", 'in') #新今宮→天王寺→寺田町

            expected = [['up', 'run']]
            actual = p0.lines[11623].joins[(0,1)].records
            self.assertEqual(expected, actual)

            expected = []
            actual = p0.lines[11623].joins[(1,2)].records
            self.assertEqual(expected, actual)

            expected = []
            actual = p0.lines[11623].joins[(17,18)].records
            self.assertEqual(expected, actual)

            expected = [['up', 'run']]
            actual = p0.lines[11623].joins[(18,0)].records
            self.assertEqual(expected, actual)

    unittest.main()
