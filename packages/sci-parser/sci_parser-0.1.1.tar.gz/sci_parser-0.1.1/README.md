# Sci Parser

[![PyPI version](https://badge.fury.io/py/sci-parser.svg)](https://badge.fury.io/py/sci-parser)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/sci-parser)](https://pypi.org/project/sci-parser/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sci-parser)](https://pypi.org/project/sci-parser/)

A parser design for extract data from the unstructured output of scientific software.

## Installation

```bash
pip install sci-parser
```

## Examples

### Parse the output of Multiwfn

Sample: [multiwfn-01.txt](tests/data/multiwfn-01.txt)

```python
from sci_parser.parser import Parser
from pprint import pprint

parser = (
    Parser()
    .kv_search('Total/Alpha/Beta electrons', v_type=float)
    .kv_search('Net charge', v_type=float)
    .kv_search('Expected multiplicity', v_type=int)
    .kv_search('Atoms', stop_at=',', v_type=int)
    .kv_search('Basis functions', stop_at=',', v_type=int)
    .kv_search('GTFs', v_type=int)
    .kv_search('Total energy', v_type=float)
    .kv_search('Virial ratio', v_type=float)
    .kv_search('Formula', value=r'(.*?)  ')
    .kv_search('Total atoms', v_type=int)
    .kv_search('Molecule weight', v_type=float)
    .kv_search('Atom list', multiline=True, stop_at='Note')
    .kv_search('Molecular planarity parameter (MPP)', value=r'(.*)$', sep='is')
)

with open('tests/data/multiwfn-01.txt') as fp:
    text = fp.read()
result = list(parser.parses(text))
pprint(result, width=120)
```

The output of the above code will be like the below

```text
[('Total/Alpha/Beta electrons', 112.0),
 ('Net charge', 0.0),
 ('Expected multiplicity', 1),
 ('Atoms', 25),
 ('Basis functions', 293),
 ('GTFs', 517),
 ('Total energy', -992.117436714606),
 ('Virial ratio', 2.00276853),
 ('Formula', 'H11 C9 O4 P1'),
 ('Total atoms', 25),
 ('Molecule weight', 214.15535),
 ('Atom list',
  '1(P ) --> Charge: 15.000000  x,y,z(Bohr):   0.178686   1.913277   0.237251\n'
  '    2(O ) --> Charge:  8.000000  x,y,z(Bohr):  -8.152243  -2.339458   1.431278\n'
  '    3(C ) --> Charge:  6.000000  x,y,z(Bohr):  -6.969052  -1.306063  -0.203009\n'
  '    4(C ) --> Charge:  6.000000  x,y,z(Bohr):  -4.964431   0.698255   0.252234\n'
  '    5(C ) --> Charge:  6.000000  x,y,z(Bohr):  -2.306306  -0.450518  -0.036829\n'
  '    6(O ) --> Charge:  8.000000  x,y,z(Bohr):  -0.017658   4.066113  -1.573236\n'
  '    7(O ) --> Charge:  8.000000  x,y,z(Bohr):  -0.156407   2.628518   3.220584\n'
  '    8(C ) --> Charge:  6.000000  x,y,z(Bohr):   3.169999   0.255647   0.041310\n'
  '    9(C ) --> Charge:  6.000000  x,y,z(Bohr):   3.926020  -1.429692   1.938584\n'
  '   10(C ) --> Charge:  6.000000  x,y,z(Bohr):   6.205681  -2.721758   1.714089\n'
  '   11(C ) --> Charge:  6.000000  x,y,z(Bohr):   7.736853  -2.337270  -0.398033\n'
  '   12(C ) --> Charge:  6.000000  x,y,z(Bohr):   6.994777  -0.654194  -2.284029\n'
  '   13(C ) --> Charge:  6.000000  x,y,z(Bohr):   4.714317   0.643294  -2.069900\n'
  '   14(O ) --> Charge:  8.000000  x,y,z(Bohr):  -7.323002  -1.977595  -2.656498\n'
  '   15(H ) --> Charge:  1.000000  x,y,z(Bohr):  -5.221096   1.420890   2.161586\n'
  '   16(H ) --> Charge:  1.000000  x,y,z(Bohr):  -5.203127   2.273013  -1.067921\n'
  '   17(H ) --> Charge:  1.000000  x,y,z(Bohr):  -2.048148  -1.321744  -1.894625\n'
  '   18(H ) --> Charge:  1.000000  x,y,z(Bohr):  -1.987820  -1.924367   1.374353\n'
  '   19(H ) --> Charge:  1.000000  x,y,z(Bohr):   0.862508   4.044165   3.765548\n'
  '   20(H ) --> Charge:  1.000000  x,y,z(Bohr):   2.750383  -1.710691   3.594765\n'
  '   21(H ) --> Charge:  1.000000  x,y,z(Bohr):   6.791898  -4.021810   3.187218\n'
  '   22(H ) --> Charge:  1.000000  x,y,z(Bohr):   9.513719  -3.346808  -0.568826\n'
  '   23(H ) --> Charge:  1.000000  x,y,z(Bohr):   8.193501  -0.346968  -3.918830\n'
  '   24(H ) --> Charge:  1.000000  x,y,z(Bohr):   4.131055   1.971614  -3.517319\n'
  '   25(H ) --> Charge:  1.000000  x,y,z(Bohr):  -6.315838  -0.943282  -3.778241\n'
  ' '),
 ('Molecular planarity parameter (MPP)', '1.109487 Angstrom')]
```
