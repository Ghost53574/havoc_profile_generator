#!/usr/bin/python3
import argparse
import sys

from modules import generator
from modules import writer
from modules import util
from modules.enum import Arch

Profile   = generator.Profile
Generator = generator.Generator
Writer    = writer.Writer

BANNER = '''
           [49m        [38;2;6;6;6;49m▄▄[38;2;6;6;6;48;2;7;7;7m▄[38;2;6;6;6;48;2;5;5;5m▄[48;2;5;5;5m  [38;2;5;5;5;48;2;4;4;4m▄[48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄▄[48;2;3;3;3m   [38;2;3;3;3;48;2;2;2;2m▄▄[48;2;2;2;2m     [38;2;2;2;2;48;2;1;1;1m▄[48;2;1;1;1m      [38;2;1;1;1;48;2;2;2;2m▄[38;2;1;1;1;49m▄[38;2;0;0;0;49m▄[49m        [m
           [49m     [38;2;8;8;8;49m▄[38;2;8;8;8;48;2;7;7;7m▄▄[48;2;7;7;7m [38;2;7;7;7;48;2;6;6;6m▄▄[48;2;6;6;6m  [38;2;6;6;6;48;2;5;5;5m▄[48;2;5;5;5m   [38;2;5;5;5;48;2;4;4;4m▄[48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄▄[48;2;3;3;3m    [38;2;3;3;3;48;2;2;2;2m▄[48;2;2;2;2m     [38;2;2;2;2;48;2;1;1;1m▄[48;2;1;1;1m       [38;2;1;1;1;48;2;0;0;0m▄[38;2;0;0;0;49m▄[49m     [m
           [49m   [38;2;10;10;10;49m▄[48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄[48;2;8;8;8m  [38;2;8;8;8;48;2;7;7;7m▄[48;2;7;7;7m  [38;2;7;7;7;48;2;6;6;6m▄▄[48;2;6;6;6m  [38;2;6;6;6;48;2;5;5;5m▄[48;2;5;5;5m   [38;2;5;5;5;48;2;4;4;4m▄[48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄▄[48;2;3;3;3m   [38;2;3;3;3;48;2;2;2;2m▄▄[38;2;255;255;255;48;2;2;2;2m▄▄[48;2;2;2;2m  [38;2;2;2;2;48;2;1;1;1m▄▄[48;2;1;1;1m       [38;2;1;1;1;49m▄[49m   [m
           [49m  [38;2;11;11;11;48;2;10;10;10m▄▄[48;2;10;10;10m [38;2;10;10;10;48;2;9;9;9m▄▄[48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄[48;2;8;8;8m  [38;2;8;8;8;48;2;7;7;7m▄[48;2;7;7;7m  [38;2;7;7;7;48;2;6;6;6m▄▄[48;2;6;6;6m  [38;2;6;6;6;48;2;5;5;5m▄[48;2;5;5;5m   [38;2;5;5;5;48;2;4;4;4m▄[48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄▄[48;2;3;3;3m  [48;2;255;255;255m  [38;2;3;3;3;48;2;2;2;2m▄[48;2;2;2;2m    [38;2;2;2;2;48;2;1;1;1m▄▄[48;2;1;1;1m      [49m  [m
           [49m [38;2;13;13;13;48;2;12;12;12m▄[48;2;12;12;12m [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m  [38;2;11;11;11;48;2;10;10;10m▄[48;2;10;10;10m [38;2;10;10;10;48;2;9;9;9m▄▄[48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄[48;2;8;8;8m  [48;2;255;255;255m  [48;2;7;7;7m [38;2;7;7;7;48;2;6;6;6m▄▄[48;2;6;6;6m  [38;2;6;6;6;48;2;5;5;5m▄[48;2;5;5;5m   [38;2;5;5;5;48;2;4;4;4m▄[48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄[48;2;255;255;255m  [48;2;3;3;3m  [38;2;3;3;3;48;2;2;2;2m▄▄[48;2;2;2;2m    [38;2;2;2;2;48;2;1;1;1m▄▄[48;2;1;1;1m    [49m [m
           [48;2;14;14;14m [38;2;14;14;14;48;2;13;13;13m▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄▄[48;2;12;12;12m [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m  [38;2;11;11;11;48;2;10;10;10m▄[48;2;10;10;10m [38;2;10;10;10;48;2;9;9;9m▄▄[48;2;9;9;9m  [48;2;255;255;255m  [48;2;8;8;8m [38;2;8;8;8;48;2;7;7;7m▄[48;2;7;7;7m  [38;2;7;7;7;48;2;6;6;6m▄[48;2;6;6;6m   [38;2;6;6;6;48;2;5;5;5m▄[48;2;5;5;5m   [38;2;5;5;5;48;2;4;4;4m▄[48;2;4;4;4m [48;2;255;255;255m  [38;2;4;4;4;48;2;3;3;3m▄[48;2;3;3;3m    [38;2;3;3;3;48;2;2;2;2m▄▄[48;2;2;2;2m    [38;2;2;2;2;48;2;1;1;1m▄▄[48;2;1;1;1m [38;2;1;1;1;48;2;2;2;2m▄[m
           [48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄[48;2;14;14;14m [38;2;14;14;14;48;2;13;13;13m▄▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄[48;2;12;12;12m  [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m [38;2;11;11;11;48;2;10;10;10m▄▄[48;2;10;10;10m [38;2;10;10;10;48;2;9;9;9m▄[48;2;255;255;255m  [38;2;9;9;9;48;2;8;8;8m▄▄[48;2;8;8;8m  [38;2;8;8;8;48;2;7;7;7m▄[48;2;7;7;7m  [38;2;7;7;7;48;2;6;6;6m▄[48;2;6;6;6m   [38;2;6;6;6;48;2;5;5;5m▄[48;2;5;5;5m  [48;2;255;255;255m  [48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄[48;2;3;3;3m    [38;2;3;3;3;48;2;2;2;2m▄[48;2;2;2;2m     [38;2;2;2;2;48;2;1;1;1m▄[m
           [38;2;17;17;17;48;2;16;16;16m▄[38;2;16;16;16;48;2;15;15;15m▄▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄[48;2;14;14;14m [38;2;14;14;14;48;2;13;13;13m▄▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄[48;2;12;12;12m  [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m [38;2;11;11;11;48;2;10;10;10m▄[48;2;255;255;255m  [38;2;10;10;10;48;2;9;9;9m▄▄[48;2;9;9;9m [38;2;9;9;9;48;2;8;8;8m▄▄[48;2;8;8;8m  [38;2;8;8;8;48;2;7;7;7m▄[48;2;7;7;7m  [38;2;234;234;234;48;2;6;6;6m▄[38;2;229;229;229;48;2;6;6;6m▄[48;2;6;6;6m  [48;2;255;255;255m  [48;2;5;5;5m [38;2;5;5;5;48;2;4;4;4m▄▄[48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄[48;2;3;3;3m    [38;2;3;3;3;48;2;2;2;2m▄[48;2;2;2;2m   [m
           [38;2;18;18;18;48;2;17;17;17m▄[48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄▄[38;2;16;16;16;48;2;15;15;15m▄▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄[48;2;14;14;14m [38;2;14;14;14;48;2;13;13;13m▄▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄[48;2;12;12;12m [38;2;12;12;12;48;2;11;11;11m▄[48;2;255;255;255m  [38;2;11;11;11;48;2;10;10;10m▄▄[48;2;10;10;10m [38;2;10;10;10;48;2;9;9;9m▄▄[48;2;9;9;9m [38;2;9;9;9;48;2;8;8;8m▄[38;2;255;255;255;48;2;8;8;8m▄[38;2;255;255;255;48;2;112;112;112m▄[48;2;255;255;255m [38;2;25;25;25;48;2;255;255;255m▄[38;2;7;7;7;48;2;251;251;251m▄[48;2;7;7;7m [38;2;223;223;223;48;2;6;6;6m▄[48;2;255;255;255m  [38;2;6;6;6;48;2;5;5;5m▄▄[48;2;5;5;5m  [38;2;5;5;5;48;2;4;4;4m▄▄[48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄[48;2;3;3;3m    [38;2;3;3;3;48;2;2;2;2m▄[m
           [38;2;19;19;19;48;2;18;18;18m▄▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄[48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄[48;2;16;16;16m [38;2;16;16;16;48;2;15;15;15m▄▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄[48;2;14;14;14m [38;2;14;14;14;48;2;13;13;13m▄▄[48;2;13;13;13m [48;2;255;255;255m  [38;2;12;12;12;48;2;11;11;11m▄▄[48;2;11;11;11m [38;2;190;190;190;48;2;10;10;10m▄[38;2;255;255;255;48;2;10;10;10m▄[48;2;255;255;255m [38;2;217;217;217;48;2;255;255;255m▄[38;2;9;9;9;48;2;255;255;255m▄[38;2;9;9;9;48;2;118;118;118m▄[38;2;15;15;15;48;2;8;8;8m▄[38;2;255;255;255;48;2;8;8;8m▄[38;2;255;255;255;48;2;83;83;83m▄[48;2;255;255;255m [38;2;34;34;34;48;2;255;255;255m▄[38;2;7;7;7;48;2;251;251;251m▄[48;2;7;7;7m [38;2;7;7;7;48;2;6;6;6m▄[48;2;6;6;6m  [38;2;6;6;6;48;2;5;5;5m▄▄[48;2;5;5;5m  [38;2;5;5;5;48;2;4;4;4m▄▄[48;2;4;4;4m   [38;2;4;4;4;48;2;3;3;3m▄[48;2;3;3;3m  [m
           [48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄▄[38;2;19;19;19;48;2;18;18;18m▄▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄[48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄[48;2;16;16;16m [38;2;16;16;16;48;2;15;15;15m▄[48;2;15;15;15m  [38;2;15;15;15;48;2;14;14;14m▄[48;2;14;14;14m [48;2;255;255;255m  [38;2;255;255;255;48;2;13;13;13m▄[38;2;255;255;255;48;2;80;80;80m▄[48;2;255;255;255m [38;2;27;27;27;48;2;255;255;255m▄[38;2;12;12;12;48;2;255;255;255m▄[38;2;11;11;11;48;2;14;14;14m▄[38;2;186;186;186;48;2;10;10;10m▄[38;2;255;255;255;48;2;10;10;10m▄[38;2;255;255;255;48;2;245;245;245m▄[38;2;233;233;233;48;2;255;255;255m▄[38;2;9;9;9;48;2;255;255;255m▄[38;2;9;9;9;48;2;119;119;119m▄[38;2;9;9;9;48;2;8;8;8m▄▄[48;2;8;8;8m [38;2;8;8;8;48;2;7;7;7m▄▄[48;2;7;7;7m  [38;2;7;7;7;48;2;6;6;6m▄[48;2;6;6;6m  [38;2;6;6;6;48;2;5;5;5m▄▄[48;2;5;5;5m  [38;2;5;5;5;48;2;4;4;4m▄▄[48;2;4;4;4m   [m
           [38;2;22;22;22;48;2;21;21;21m▄[48;2;21;21;21m [38;2;21;21;21;48;2;20;20;20m▄[48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄▄[38;2;19;19;19;48;2;18;18;18m▄▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄[48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄[48;2;16;16;16m [38;2;16;16;16;48;2;15;15;15m▄[48;2;15;15;15m [48;2;255;255;255m [38;2;249;249;249;48;2;255;255;255m▄[38;2;14;14;14;48;2;255;255;255m▄[38;2;14;14;14;48;2;146;146;146m▄[38;2;14;14;14;48;2;13;13;13m▄[48;2;13;13;13m [38;2;255;255;255;48;2;77;77;77m▄[48;2;255;255;255m [38;2;49;49;49;48;2;255;255;255m▄[38;2;12;12;12;48;2;255;255;255m▄[48;2;11;11;11m [38;2;17;17;17;48;2;10;10;10m▄[38;2;11;11;11;48;2;10;10;10m▄[48;2;10;10;10m [38;2;10;10;10;48;2;9;9;9m▄[48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄▄[48;2;8;8;8m [38;2;8;8;8;48;2;7;7;7m▄▄[48;2;7;7;7m  [38;2;7;7;7;48;2;6;6;6m▄[48;2;6;6;6m  [38;2;6;6;6;48;2;5;5;5m▄▄[48;2;5;5;5m  [38;2;5;5;5;48;2;4;4;4m▄▄[m
           [48;2;22;22;22m   [38;2;22;22;22;48;2;21;21;21m▄[48;2;21;21;21m [38;2;21;21;21;48;2;20;20;20m▄[48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄[48;2;19;19;19m [38;2;19;19;19;48;2;18;18;18m▄▄[38;2;18;18;18;48;2;17;17;17m▄▄[48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄[48;2;16;16;16m [38;2;16;16;16;48;2;15;15;15m▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄▄[48;2;14;14;14m [38;2;14;14;14;48;2;19;19;19m▄[48;2;13;13;13m [38;2;255;255;255;48;2;13;13;13m▄[38;2;255;255;255;48;2;49;49;49m▄[48;2;255;255;255m [38;2;77;77;77;48;2;255;255;255m▄[48;2;11;11;11m  [38;2;151;151;151;48;2;10;10;10m▄[38;2;255;255;255;48;2;10;10;10m▄[38;2;255;255;255;48;2;249;249;249m▄[48;2;255;255;255m [48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄[48;2;8;8;8m  [38;2;8;8;8;48;2;7;7;7m▄▄[48;2;7;7;7m [38;2;7;7;7;48;2;6;6;6m▄▄[48;2;6;6;6m  [38;2;6;6;6;48;2;5;5;5m▄▄[48;2;5;5;5m [m
           [48;2;22;22;22m      [38;2;22;22;22;48;2;21;21;21m▄[48;2;21;21;21m [38;2;21;21;21;48;2;20;20;20m▄[48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄[48;2;19;19;19m [38;2;19;19;19;48;2;18;18;18m▄▄[38;2;18;18;18;48;2;17;17;17m▄▄[48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄[48;2;16;16;16m [38;2;124;124;124;48;2;15;15;15m▄[38;2;255;255;255;48;2;15;15;15m▄[38;2;255;255;255;48;2;234;234;234m▄[38;2;245;245;245;48;2;255;255;255m▄[38;2;14;14;14;48;2;255;255;255m▄[38;2;14;14;14;48;2;186;186;186m▄[38;2;16;16;16;48;2;13;13;13m▄[38;2;255;255;255;48;2;13;13;13m▄[38;2;255;255;255;48;2;27;27;27m▄[48;2;255;255;255m [38;2;80;80;80;48;2;255;255;255m▄[38;2;12;12;12;48;2;255;255;255m▄[48;2;255;255;255m  [48;2;10;10;10m  [38;2;10;10;10;48;2;9;9;9m▄[48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄[48;2;8;8;8m  [38;2;8;8;8;48;2;7;7;7m▄▄[48;2;7;7;7m [38;2;7;7;7;48;2;6;6;6m▄▄[48;2;6;6;6m  [m
           [48;2;22;22;22m         [38;2;22;22;22;48;2;21;21;21m▄[48;2;21;21;21m [38;2;21;21;21;48;2;20;20;20m▄[48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄[48;2;19;19;19m [38;2;19;19;19;48;2;18;18;18m▄[38;2;251;251;251;48;2;18;18;18m▄[38;2;255;255;255;48;2;42;42;42m▄[48;2;255;255;255m [38;2;89;89;89;48;2;255;255;255m▄[38;2;17;17;17;48;2;255;255;255m▄[38;2;16;16;16;48;2;22;22;22m▄[38;2;128;128;128;48;2;15;15;15m▄[38;2;255;255;255;48;2;15;15;15m▄[38;2;255;255;255;48;2;218;218;218m▄[48;2;255;255;255m [38;2;14;14;14;48;2;255;255;255m▄[38;2;14;14;14;48;2;184;184;184m▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄▄[48;2;255;255;255m  [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m [38;2;11;11;11;48;2;10;10;10m▄[48;2;10;10;10m  [38;2;10;10;10;48;2;9;9;9m▄[48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄[48;2;8;8;8m  [38;2;8;8;8;48;2;7;7;7m▄▄[48;2;7;7;7m [38;2;7;7;7;48;2;6;6;6m▄[m
           [48;2;22;22;22m            [38;2;22;22;22;48;2;21;21;21m▄[48;2;21;21;21m [38;2;21;21;21;48;2;20;20;20m▄[48;2;255;255;255m  [38;2;19;19;19;48;2;225;225;225m▄[38;2;19;19;19;48;2;18;18;18m▄[38;2;251;251;251;48;2;18;18;18m▄[38;2;255;255;255;48;2;34;34;34m▄[48;2;255;255;255m [38;2;117;117;117;48;2;255;255;255m▄[38;2;17;17;17;48;2;255;255;255m▄[48;2;16;16;16m [38;2;16;16;16;48;2;15;15;15m▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄▄[48;2;14;14;14m [38;2;14;14;14;48;2;13;13;13m▄[48;2;255;255;255m  [38;2;13;13;13;48;2;12;12;12m▄[48;2;12;12;12m [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m  [38;2;11;11;11;48;2;10;10;10m▄[48;2;10;10;10m  [38;2;10;10;10;48;2;9;9;9m▄[48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄[48;2;8;8;8m  [38;2;8;8;8;48;2;7;7;7m▄[m
           [48;2;22;22;22m               [48;2;255;255;255m  [38;2;21;21;21;48;2;20;20;20m▄[48;2;20;20;20m [38;2;20;20;20;48;2;231;231;231m▄[38;2;19;19;19;48;2;235;235;235m▄[38;2;19;19;19;48;2;18;18;18m▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄▄[38;2;17;17;17;48;2;16;16;16m▄▄[48;2;16;16;16m [38;2;16;16;16;48;2;15;15;15m▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄[48;2;255;255;255m  [38;2;14;14;14;48;2;13;13;13m▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄▄[48;2;12;12;12m [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m  [38;2;11;11;11;48;2;10;10;10m▄[48;2;10;10;10m  [38;2;10;10;10;48;2;9;9;9m▄[48;2;9;9;9m  [38;2;9;9;9;48;2;8;8;8m▄[m
           [48;2;22;22;22m               [48;2;255;255;255m  [48;2;22;22;22m [38;2;22;22;22;48;2;21;21;21m▄[38;2;21;21;21;48;2;20;20;20m▄▄[48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄[48;2;19;19;19m [38;2;19;19;19;48;2;18;18;18m▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄▄[38;2;17;17;17;48;2;16;16;16m▄▄[38;2;16;16;16;48;2;15;15;15m▄[48;2;255;255;255m  [38;2;15;15;15;48;2;14;14;14m▄▄[48;2;14;14;14m [38;2;14;14;14;48;2;13;13;13m▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄▄[48;2;12;12;12m [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m  [38;2;11;11;11;48;2;10;10;10m▄[48;2;10;10;10m [38;2;10;10;10;48;2;9;9;9m▄▄[m
           [38;2;23;23;23;48;2;22;22;22m▄[48;2;22;22;22m              [48;2;255;255;255m  [48;2;22;22;22m   [38;2;22;22;22;48;2;21;21;21m▄▄[38;2;21;21;21;48;2;20;20;20m▄▄[48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄[48;2;19;19;19m [38;2;19;19;19;48;2;18;18;18m▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄[48;2;17;17;17m [48;2;255;255;255m  [38;2;16;16;16;48;2;15;15;15m▄▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄[48;2;14;14;14m  [38;2;14;14;14;48;2;13;13;13m▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄[48;2;12;12;12m  [38;2;12;12;12;48;2;11;11;11m▄[48;2;11;11;11m  [38;2;11;11;11;48;2;10;10;10m▄[m
           [49m [48;2;22;22;22m              [48;2;255;255;255m  [48;2;22;22;22m      [38;2;22;22;22;48;2;21;21;21m▄▄[38;2;21;21;21;48;2;20;20;20m▄▄[48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄[48;2;19;19;19m [38;2;19;19;19;48;2;18;18;18m▄[48;2;255;255;255m  [48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄▄[38;2;16;16;16;48;2;15;15;15m▄▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄[48;2;14;14;14m  [38;2;14;14;14;48;2;13;13;13m▄[48;2;13;13;13m [38;2;13;13;13;48;2;12;12;12m▄▄[48;2;12;12;12m [49m [m
           [49m  [48;2;22;22;22m             [48;2;255;255;255m  [48;2;22;22;22m         [38;2;22;22;22;48;2;21;21;21m▄▄[38;2;21;21;21;48;2;20;20;20m▄▄[38;2;20;20;20;48;2;19;19;19m▄▄[48;2;19;19;19m [38;2;19;19;19;48;2;18;18;18m▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄[48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄▄[38;2;16;16;16;48;2;15;15;15m▄▄[48;2;15;15;15m [38;2;15;15;15;48;2;14;14;14m▄[48;2;14;14;14m [38;2;14;14;14;48;2;13;13;13m▄[48;2;13;13;13m [49m  [m
           [49m   [49;38;2;22;22;22m▀[48;2;22;22;22m           [38;2;22;22;22;48;2;255;255;255m▄▄[48;2;22;22;22m            [38;2;22;22;22;48;2;21;21;21m▄▄[38;2;21;21;21;48;2;20;20;20m▄▄[38;2;20;20;20;48;2;19;19;19m▄▄[38;2;19;19;19;48;2;18;18;18m▄▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄[48;2;17;17;17m [38;2;17;17;17;48;2;16;16;16m▄▄[38;2;16;16;16;48;2;15;15;15m▄▄[49;38;2;15;15;15m▀[49m   [m
           [49m     [49;38;2;22;22;22m▀[48;2;22;22;22m                          [38;2;22;22;22;48;2;21;21;21m▄▄[38;2;21;21;21;48;2;20;20;20m▄[48;2;20;20;20m [38;2;20;20;20;48;2;19;19;19m▄▄[48;2;19;19;19m [38;2;19;19;19;48;2;18;18;18m▄[48;2;18;18;18m [38;2;18;18;18;48;2;17;17;17m▄[49;38;2;17;17;17m▀[49m     [m
           [49m        [49;38;2;22;22;22m▀▀[38;2;23;23;23;48;2;22;22;22m▄[48;2;22;22;22m                        [38;2;22;22;22;48;2;21;21;21m▄▄[38;2;21;21;21;48;2;20;20;20m▄[49;38;2;20;20;20m▀[49;38;2;19;19;19m▀[49m        [m

                      Havoc C2 Profile Generator
                              by c0z\033[0m
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog='Havoc profile generator',
            description='Generate havoc c2 profiles with ease and randomness')
    parser.add_argument('-c', '--config', 
                        type=argparse.FileType('r'), 
                        required=False, 
                        help='Config file to use, don\' use a conifg file for a completely random profile')
    parser.add_argument('-r', '--read', 
                        type=str, 
                        action='store', 
                        default="Nothing", 
                        help='Directory to read CS profiles from')
    parser.add_argument('-l', '--list', 
                        type=util.str_to_bool, 
                        nargs='?', 
                        const=True, 
                        default=False, 
                        help='List supported profiles')
    parser.add_argument('-s', '--sysnative', 
                        type=util.str_to_bool, 
                        nargs='?', 
                        const=True, 
                        default=False, 
                        help='Only support sysnative for spawn to')
    parser.add_argument('-a', '--arch', 
                        type=str, 
                        action='store', 
                        default="Nothing", 
                        help='Selected architecture between x86, x64 & x86_64')
    parser.add_argument('-p', '--profile', 
                        type=str, 
                        action='store',
                        default="Nothing", 
                        help='Select a traffic profile')
    parser.add_argument('-H', '--host', 
                        type=str, 
                        action='store', 
                        default="Nothing", 
                        help='The listeners ip')
    parser.add_argument('-S', '--hosts', 
                        type=str, 
                        action='store', 
                        default="Nothing", 
                        help='The hosts array in the form of 10.0.0.1,10.0.0.2')
    parser.add_argument('-P', '--port', 
                        type=str, 
                        action='store', 
                        default="Nothing", 
                        help='Set the port for listeners to listen on')
    parser.add_argument('-L', '--listeners', 
                        type=str, 
                        action='store', 
                        default="Nothing", 
                        help='Set the port for listeners to listen on')
    parser.add_argument('-E', '--evasion', 
                        type=util.str_to_bool, 
                        nargs='?', 
                        const=True, 
                        default=False, 
                        help='Set beacon defaults to be more evasive')
    parser.add_argument('-M', '--mports', 
                        type=str, 
                        action='store', 
                        default="Nothing",
                        help='Set\'s the min port and max port for randomization')
    parser.add_argument('-o', '--outfile', 
                        type=str, 
                        action='store', 
                        default="Nothing", 
                        help='Output file of the final Havoc C2 pofile')
    parser.add_argument('-q', '--quiet', 
                        type=util.str_to_bool, 
                        nargs='?', 
                        const=True, 
                        default=False, 
                        help='Do not show banner')
    args = parser.parse_args()

    if not args.quiet:
        print(f"{BANNER}")

    template = None
    outfile = None
    config = None
    profile = None
    host = None
    hosts = None
    port = None
    arch = None
    listeners = None

    cs_profiles = None
    min_port = None
    max_port = None

    profiles = None

    loaded_profiles_data = {}

    if args.read != "Nothing":
        loaded_profiles = util.get_cs_profiles(args.read)
        loaded_profile_names = [ x.split("/")[-1] for x in list(loaded_profiles.keys()) ]
        parsed_profiles = {}
        for i, cs_profile in enumerate(loaded_profiles.keys()):
            parsed_profile_name = loaded_profile_names[i]
            parsed_profile_data = util.parse_cs_profile(profile=loaded_profiles[cs_profile], 
                                                   verb="any")
            parsed_profiles[parsed_profile_name] = parsed_profile_data
        profiles = util.Profiles(loaded_profile_names, parsed_profiles)
    else:
        profiles, loaded_profiles_data = util.load_profiles()
    
    if not profiles or not loaded_profiles_data:
        util.print_fail("Loaded profiles failed to load. Make sure there is a config directory with profile templates in it or a directory with CS profiles is specified")

    def list_profiles() -> None:
            for profile in profiles:
                util.print_good(f"Profile: {profile}")

    if args.list:
        list_profiles()
        sys.exit(0)

    if args.profile != "Nothing":
        profile = args.profile
    else:
        profile = "any"
    
    if args.arch != "Nothing":
        if args.arch == "x86_64":
            arch = Arch("x86_64")
        elif args.arch == "x64":
            arch == Arch("x64")
        elif args.arch == "x86":
            arch == Arch("x86")
    
    if args.host != "Nothing":
        host = args.host

    if args.hosts != "Nothing":
        hosts = args.hosts

    if args.port != "Nothing":
        port = args.port

    if args.mports != "Nothing":
        port_min = args.mports.split(',')[0]
        if port_min:
            min_port = port_min
        else:
            min_port = 1024
        port_max = args.mports.split(',')[1]
        if port_max:
            max_port = port_max
        else:
            max_port = 65534
    else:
        min_port = 1024
        max_port = 65534

    if args.listeners != "Nothing":
        listeners = args.listeners
    
    if args.outfile != "Nothing":
        outfile = args.outfile
    else:
        outfile = None

    if args.config:
        config = args.config.readlines()

    if not args.quiet:
        util.print_warn(f"""Options were:
    config:      {config is not None}
    sysnative:   {args.sysnative}
    evasion:     {args.evasion}
    profile:     {profile is not None}
    arch:        {arch is not None}
    host:        {host is not None}
    hosts:       {hosts is not None}
    port:        {port is not None}
    listeners:   {listeners is not None}
    outfile:     {outfile is not None}
        """)
    
    generated_profile = Profile(quiet=args.quiet,
                                profile_names=profiles,
                                profiles=loaded_profiles_data,
                                profile=profile,
                                sysnative=args.sysnative,
                                evasion=args.evasion,
                                min_port=min_port,
                                max_port=max_port,
                                config=config,
                                host=host,
                                port=port,
                                hosts=hosts,
                                extra_listeners=listeners,
                                arch=arch)

    if not args.quiet and outfile:
        util.print_good(f"Saving profile to {outfile}")
    Writer(filename=outfile).Write(profile=generated_profile.Print())
