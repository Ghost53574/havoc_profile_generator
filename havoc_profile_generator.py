#!/usr/bin/python3

from faker.factory import Factory
import ipaddress
import argparse
import random
import uuid
import json
import os
import sys
import mpp

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
INFO = '\033[92m'
WARN = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

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

Faker = Factory.create
fake = Faker()

profile_dir = "profiles"
search_path = os.environ['PATH']
windows_dir_root = "C:\\\\Windows"
windows_dir_sysnative = "\\System32"
windows_dir_syswow64 = "\\SysWow64"

# Default profile settings
all_interfaces = "0.0.0.0"
localhost = "127.0.0.1"
default_port = 40056
default_user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
default_response = [ "Content-type: text/plain; charset=utf-8", "Connection: keep-alive", "Cache-control: non-cache" ]
default_headers = [ "Content-type: text/plain; charset=utf-8", "Accept-Language: en-US" ]
default_urls = [ "/images/dog.jpg", "/images/cat.jpg", "/images/dolphin.jpg" ]

# Default files needed
default_compiler_x64 = "x86_64-w64-mingw32-gcc"
default_compiler_x86 = "i686-w64-mingw32-gcc"
default_assembler = "nasm"

# Default OPSEC safer programs to spawn to
default_spawnto_opsec = {
    "gpupdate": "gpupdate.exe /Target:User /Sync /Force",
    "werfault": "Werfault.exe",
    "svchost": "svchost.exe -k netsvcs",
    "dashost": "dasHost.exe ",
    "dllhost": "dllhost.exe /PROCESSID:",
    "conhost": "conhost.exe 0x4",
    "taskhostw": "taskhostw.exe "
}

default_spawnto_only_sysnative = [
    "dashost",
    "taskhostw",
    "conhost"
]

default_spawnto_all = [
    "gpupdate",
    "werfault",
    "svchost",
    "dashost",
    "dllhost",
    "conhost",
    "taskhostw"
]

default_pipenames = [
    "mojo",
    "gecko",
    "guid",
    "chrome",
    "discord",
    "shellex",
    "pshost",
    "tcppipe"
]

loaded_profiles_data = {}

# Flags
SYSNATIVE=False

# Utility functions
def str_to_bool(value):
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')

def generate_dashost_pid() -> str:
    id = uuid.uuid4().urn[9:].split("-")
    pid = f"{id[0]}-{id[1]}-{id[2]}{id[3]}{id[4]}{random.choice(range(0,9))}"
    return pid

def generate_dllhost_uuid() -> str:
    id = uuid.uuid4().urn[9:]
    return "{" + f"{id}" + "}"

def generate_pipename(process_name) -> str:
    first_part = random.choice(range(4000,20000))
    second_part = random.choice(range(4000,20000))
    third_part = random.choice(range(100000000,9999999999))
    fourth_part = random.choice(range(100000000,999999999))
    fifth_part = random.choice(range(2048, 99999))
    sixth_part = random.choice(range(400, 1024))
    if not fifth_part or not second_part or not third_part or not fourth_part or not fifth_part or not sixth_part:
        return None
    if process_name == "mojo" or process_name == "gecko":
        pipename = f"{process_name}.{first_part}.{second_part}.{third_part}{fourth_part}"
    elif process_name == "guid":
        pipename = f"{generate_dllhost_uuid()}"
    elif process_name == "chrome":
        pipename = f"{process_name}.{fifth_part}.{sixth_part}.{fourth_part}"
    elif process_name == "discord":
        pipename = f"{process_name}-ipc-{random.choice(range(1,9))}"
    elif process_name == "shellex":
        pipename = f"ShellEx_{fifth_part}"
    elif process_name == "tcppipe":
        pipename = f"{process_name}{sixth_part}"
    else:
        return None
    return pipename

def get_random_port(port = None) -> int:
    if not port:
        return random.choice(range(1025, 65534))
    else:
        return port
    
def load_profiles() -> list:
    if not os.path.isdir(profile_dir):
        return None
    for root, _, files in os.walk(profile_dir):
        loaded_profiles = files
    temp = []
    for f in loaded_profiles:
        if os.path.isfile(f"{profile_dir}/{f}"):
            name = f.split(".")[0]
            profile_data = ""
            with open(f"{profile_dir}/{f}", "r") as fe:
                profile_data = json.loads(fe.read())
            temp.append(name)
            loaded_profiles_data[name] = profile_data
    return temp

def Find(name, _search_path = None):
    if _search_path:
        paths = _search_path
    else:
        paths = search_path.split(":")
    for path in paths: 
        for root, _, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

def print_good(message):
    print(f"{INFO}[+] {message}{ENDC}")

def print_warn(message):
    print(f"{WARN}[!] {message}{ENDC}")

def print_fail(message):
    raise Exception(f"{FAIL}[x] {message}{ENDC}")

class Base:
    def Find(self, name, _search_path = None):
        if _search_path:
            paths = _search_path
        else:
            paths = search_path.split(":")
        for path in paths: 
            for root, _, files in os.walk(path):
                if name in files:
                    return os.path.join(root, name)
                
    def Get(self) -> object:
        return self
    
class Build(Base):
    def __init__(self, compiler_64=None, compiler_86=None, compiler_nasm=None) -> None:
        self.compiler_64 = None
        self.compiler_86 = None
        self.compiler_nasm = None

        if compiler_64:
            self.compiler_64 = compiler_64
        else:
            self.compiler_64 = self.Find(default_compiler_x64)
            if not self.compiler_64:
                print_fail(f"Cannot find {default_compiler_x64}")
        if compiler_86:
            self.compiler_86 = compiler_86
        else:
            self.compiler_86 = self.Find(default_compiler_x86)
            if not self.compiler_86:
                print_fail(f"Cannot find {default_compiler_x86}")
        if compiler_nasm:
            self.compiler_nasm = compiler_nasm
        else:
            self.compiler_nasm = self.Find(default_assembler)
            if not self.compiler_nasm:
                print_fail(f"Cannot find {default_assembler}")
            
    def Print(self) -> dict:
        template = {}
        if self.compiler_64:
            path = self.Find(self.compiler_64)
            if path:
                template["Compiler64"] = path
        if self.compiler_86:
            path = self.Find(self.compiler_86)
            if path:
                template["Compiler86"] = path
        if self.compiler_nasm:
            path = self.Find(self.compiler_nasm)
            if path:
                template["Nasm"] = path
        return template

class Teamserver(Base):
    def __init__(self, host, port, build: Build = None) -> None:
        self.host = host
        self.port = port
        self.build = None

        if not host or not port:
            self.host = all_interfaces
            self.port = default_port

        if build:
            self.build = build

    def Print(self) -> dict:
        template = {}
        if self.host and ipaddress.ip_address(self.host):
            template["Host"] = self.host
        if self.port and (self.port > 1 and self.port < 65535):
            template["Port"] = self.port
        if self.build:
            template["Build"] = self.build.Print()
        return template

class Operators(Base):
    def __init__(self) -> None:
        self.users = {}
    
    def Add_User(self, username, password, hashed = None) -> None:
        if username and password and not hashed:
            self.users[username] = password
        if username and password and hashed:
            self.users[username] = {password, hashed}

    def Delete_User(self, Username) -> None:
        if Username:
            for k in self.users.keys:
                if k == Username:
                    del self.users[k]
    
    def Print(self) -> dict:
        template = {}
        values = {}
        if self.users:
            for user in self.users:
                username = f"{user}"
                password = self.users[user]
                values["Password"] = password
                template[username] = values
        else:
            print_fail("No users in Operator block")
        return template
    
class Cert(Base):
    def __init__(self, cert_path, key_path) -> None:
        if os.path.isfile(cert_path):
            self.cert_path = cert_path
        else:
            print_fail("Certificate path does not exist")
        
        if os.path.isfile(key_path):
            self.key_path = key_path
        else:
            print_fail("Key path does not exist")
        
    def Print(self) -> dict:
        template = {}
        template["Cert"] = self.cert_path
        template["Key"] = self.key_path
        return template
    
class Proxy(Base):
    def __init__(self, host, port, username = None, password = None) -> None:
        self.host = host
        self.port = port
        self.username = None
        self.password = None
        if username and password:
            self.username = username
            self.password = password

    def Print(self) -> dict:
        template = {}
        template["Host"] = self.host
        template["Port"] = self.port
        if self.username and self.password:
            template["Username"] = self.username
            template["Password"] = self.password
        return template

class Response(Base):
    def __init__(self, headers) -> None:
        if headers:
            self.headers = headers

    def Print(self) -> dict:
        template = {}
        headers = []
        for header in self.headers:
            headers.append(header)
        template["Headers"] = headers
        return template
    
class Http_Listener(Cert, Base):
    host_rotation_types = [ "random", "round-robin" ]
    def __init__(self, name, hosts, port, host_bind, 
                 host_rotation = None, user_agent = None, headers = None, urls = None, secure = None, 
                 cert: Cert = None, proxy: Proxy = None, response: Response = None) -> None:
        self.name = name
        self.hosts = hosts
        self.port = port
        self.host_bind = host_bind
        self.host_rotation = None
        self.user_agent = None
        self.headers = None
        self.urls = None
        self.secure = None
        self.cert = None
        self.proxy = None
        self.reponse = None

        if host_rotation in self.host_rotation_types:
            self.host_rotation = host_rotation
        else:
            self.host_rotation = "round-robin"
        if user_agent:
            self.user_agent = user_agent
        else:
            self.user_agent = default_user_agent
        if headers:
            self.headers = headers
        else:
            self.headers = [ "Content-type: */*" ]
        if urls:
            self.urls = urls
        else:
            self.urls = [ "/" ]
        if not secure:
            self.secure = secure
        else:
            self.secure = "false"
        if cert:
            self.cert = cert
        if proxy:
            self.proxy = proxy
        if response:
            self.reponse = response
        else:
            self.reponse = Response(default_headers)

    def Print(self) -> dict:
        template = {}
        template["Name"] = self.name
        template["Port"] = self.port
        template["Hosts"] = self.hosts
        template["HostBind"] = self.host_bind
        if self.host_rotation:
            template["HostRotation"] = self.host_rotation
        else:
            template["HostRotation"] = "round-robin"
        if self.secure:
            template["Secure"] = "true"
        else:
            template["Secure"] = "false"
        template["UserAgent"] = self.user_agent
        template["Urls"] = self.urls
        template["Headers"] = self.headers
        if self.cert:
            template["Cert"] = self.cert.Print()
        if self.proxy:
            template["Proxy"] = self.proxy.Print()
        if self.reponse:
            template["Response"] = self.reponse.Print()
        return template

class Smb_Listener(Cert, Base):
    host_rotation_types = [ "random", "round-robin" ]
    def __init__(self, name = None, pipename = None) -> None:
        self.name = None
        self.pipename = None

        if name:
            self.name = name
        else:
            self.name = str(fake.name()).split(" ")[1]

        if pipename:
            self.pipename = pipename
        else:
            temp = ""
            while not temp:
                temp = generate_pipename(random.choice(default_pipenames))
            if temp:
                self.pipename = temp
            else:
                print_fail("Failed to generate pipename")

    def Print(self) -> dict:
        template = {}
        template["Name"] = self.name
        template["Pipename"] = self.pipename
        return template

class External_Listener(Cert, Base):
    def __init__(self, name, endpoint) -> None:
        self.name = name
        self.endpoint = endpoint

    def Print(self) -> dict:
        template = {}
        template["Name"] = self.name
        template["Endpoint"] = self.endpoint
        return template

class Listeners(Http_Listener, Smb_Listener):
    def __init__(self) -> None:
        self.http_listeners = []
        self.smb_listeners = []
        self.ext_listeners = []
    
    def Add_Http_Listener(self, listener: Http_Listener) -> None:
        self.http_listeners.append(listener.Print())

    def Add_Smb_Listener(self, listener: Smb_Listener) -> None:
        self.smb_listeners.append(listener.Print())

    def Add_External_Listener(self, listener: External_Listener) -> None:
        self.ext_listeners.append(listener.Print())

    def Print(self):
        listeners = []
        for listener in self.http_listeners:
            listener_dict = {}
            listener_dict["Http"] = listener
            listeners.append(listener_dict)
        for listener in self.smb_listeners:
            listener_dict = {}
            listener_dict["Smb"] = listener
            listeners.append(listener_dict)
        for listener in self.ext_listeners:
            listener_dict = {}
            listener_dict["External"] = listener
            listeners.append(listener_dict)
        return listeners

    def Get(self) -> object:
        return self

class Injection(Base):
    ARCH_X86 = "x86"
    ARCH_X64 = "x64"
    ARCH_SYSWOW = "x86_64"

    def __init__(self, spawn_x64 = None, spawn_x86 = None, arch = None) -> None:
        self.sysnative_binary = None
        self.syswow_binary = None

        if arch == "both":
            self.syswow_binary = self.Random(self.ARCH_SYSWOW)
            self.sysnative_binary = self.Random(self.ARCH_X64)
        elif arch == "x64":
            self.sysnative_binary = self.Random(self.ARCH_X64)
        elif arch == "x86":
            self.sysnative_binary = self.Random(self.ARCH_X86)
        else:
            self.sysnative_binary = self.Random(self.ARCH_X86)

        if spawn_x64:
            self.spawn_x64 = spawn_x64
        else:
            if not SYSNATIVE and arch == "both":
                self.spawn_x64 = self.syswow_binary
            elif not SYSNATIVE and arch == "x64":
                self.spawn_x64 = self.sysnative_binary
            else:
                self.spawn_x64 = self.sysnative_binary

        if spawn_x86:
            self.spawn_x86 = spawn_x86
        else:
            if not SYSNATIVE and arch == "both":
                self.spawn_x86 = self.syswow_binary
            elif not SYSNATIVE and arch == "x86":
                self.spawn_x86 = self.sysnative_binary
            else:
                self.spawn_x86 = self.sysnative_binary

    def Random(self, arch) -> str:
        if arch == self.ARCH_X64:
            windows_dir = f"{windows_dir_root}\\{windows_dir_sysnative}\\"
        elif arch == self.ARCH_X86:
            windows_dir = f"{windows_dir_root}\\{windows_dir_sysnative}\\"
        elif arch == self.ARCH_SYSWOW:
            windows_dir = f"{windows_dir_root}\\{windows_dir_syswow64}\\"
        else:
            return None
        
        if arch == self.ARCH_SYSWOW:
            prog = random.choice(default_spawnto_all)
        else:
            prog = random.choice(default_spawnto_only_sysnative)

        spawn_to = f"{windows_dir}\\{default_spawnto_opsec[prog]}"

        if prog == "dashost":
            spawn_to = f"{spawn_to}{generate_dashost_pid()}"
        elif prog == "dllhost":
            spawn_to = f"{spawn_to}{generate_dllhost_uuid()}"
        
        return spawn_to

    def Print(self) -> dict:
        template = {}
        template["Spawn64"] = self.spawn_x64
        template["Spawn86"] = self.spawn_x86
        return template

class Binary(Base):
    def __init__(self) -> None:
        pass

    def Print(self) -> dict:
        pass

class Demon(Base):
    def __init__(self, sleep, jitter, injection: Injection = None) -> None:
        self.sleep = None
        self.injection = None

        if sleep:
            self.sleep = sleep
        else:
            self.sleep = 10
        if jitter:
            self.jitter = jitter
        else:
            self.jitter = 15
        if injection:
            self.injection = injection
        else:
            self.injection = Injection(None, None)

    def Print(self) -> dict:
        template = {}
        template["Sleep"] = self.sleep
        template["Jitter"] = self.jitter
        if self.injection:
            template["Injection"] = self.injection.Print()
        return template

class Service(Base):
    def __init__(self, endpoint, password) -> None:
        if endpoint and password:
            self.endpoint = endpoint
            self.password = password
    
    def Print(self) -> dict:
        template = {}
        template["Endpoint"] = self.endpoint
        template["Password"] = self.password
        return template
    
# Will define Webhook when more webhooks come out

class Generator(Teamserver, Operators, Listeners, Demon, Service):
    def __init__(self, teamserver: Teamserver, operators: Operators, listeners: Listeners, demon: Demon, service: Service = None) -> None:
        self.service = None

        if teamserver:
            self.teamserver = teamserver
        else:
            print_fail("Need a teamserver config")
        if operators:
            self.operators = operators
        else:
            print_fail("Need at least one operator config")
        if listeners:
            self.listeners = listeners
        else:
            print_fail("Need a listener config")
        if Service:
            self.service = service
        if demon:
            self.demon = demon
        else:
            print_fail("Need a demon config")

    def Print(self) -> dict:
        template = {}
        if self.teamserver:
            template["Teamserver"] = self.teamserver.Print()
        else:
            print_fail("Need a Teamserver config")
        if self.operators:
            template["Operators"] = self.operators.Print()
        else:
            print_fail("Need at least one Operator config")
        if self.listeners:
            template["Listeners"] = self.listeners.Print()
        else:
            print_fail("Need a Listeners block in config")
        if self.service:
            template["Service"] = self.service.Print()
        if self.demon:
            template["Demon"] = self.demon.Print()
        else:
            print_fail("Need a Demon block in config")
        return template

    def Get(self) -> object:
        return self
    
class Profile():
    def __init__(self, quiet, profiles, profile = None, config = None, host = None, port = None, hosts = None, arch = None) -> object:
        self.profile = None
        self.config = None

        operator_block = None
        listeners_block = None
        service_block = None
        demon_block = None

        print_good("Generating profile")

        if profile:
            self.profile = profile
        else:
            self.profile = random.choice(profiles)

        if config:
            self.config = json.loads("".join(config))
            teamserver_host = self.config.get("ts_host")
            teamserver_port = self.config.get("ts_port")
            build_compiler_x64 = self.config.get("compiler_x64")
            build_compiler_x86 = self.config.get("compiler_x86")
            build_assembler = self.config.get("assembler")

            operator_block = self.config.get("users")
            listeners_block = self.config.get("listeners")
            service_block = self.config.get("service")
            demon_block = self.config.get("demon")
        else:
            teamserver_host = localhost
            teamserver_port = get_random_port()
            build_compiler_x64 = default_compiler_x64
            build_compiler_x86 = default_compiler_x86
            build_assembler = default_assembler

        if not teamserver_host and not teamserver_port:
            teamserver_host = localhost
            teamserver_port = default_port
        elif not teamserver_host:
            teamserver_host = localhost
        elif not teamserver_port:
            teamserver_port = default_port
        if not build_compiler_x64 and not build_compiler_x86:
            build_compiler_x64 = default_compiler_x64
            build_compiler_x86 = default_compiler_x86
        elif build_compiler_x86 and not build_compiler_x64:
            build_compiler_x64 = default_compiler_x64
        elif build_compiler_x64 and not build_compiler_x86:
            build_compiler_x86 = default_compiler_x86

        if not build_assembler:
            build_assembler = default_assembler

        if not quiet:
            print("")
            print_warn(f"""Teamserver options:
    Host: {teamserver_host}
    Port: {teamserver_port}

Build options:
    Compiler_x64: {build_compiler_x64}
    Compiler x86: {build_compiler_x86}
    Nasm:         {build_assembler}
        """)

        build = Build(build_compiler_x64, build_compiler_x86, build_assembler)
        teamserver = Teamserver(teamserver_host, teamserver_port, build)
        print_good("Teamserver built")

        if not quiet:
            print("")
            print_warn("Getting users")
        if not operator_block:
            operators = Operators()
            random_uesrname = fake.user_name()
            random_password = fake.password()
            operators.Add_User(random_uesrname, random_password)
        else:
            operators = Operators()
            for op in operator_block:
                operator_user = dict(op).keys()
                for key in operator_user:
                    username = key
                    password = dict(op)[key]
                    operators.Add_User(username, password)

        if not quiet:
            print_operator = dict(operators.Print())
            for key in print_operator.keys():
                print_user = key
                print_pass = print_operator[key]["Password"]
                print_warn(f"""Operator users:
    user: {print_user}
    pass: {print_pass}
                """)
        print_good("Generated Operators")

        if not profile or profile == "any":
            selected_profile = random.choice(profiles)
        elif profile == "none":
            selected_profile = None
            profile_data = None
        else:
            selected_profile = profile

        if selected_profile:
            profile_data = loaded_profiles_data[selected_profile]
        else:
            print_warn("No profile selected, using config data")

        profile_request = None
        profile_response = None
        profile_headers = None

        if profile_data:
            profile_request = profile_data.get("Request")
            profile_response = profile_data.get("Response")
            profile_headers = profile_data.get("Headers")

        listeners = Listeners()

        if not listeners_block:
            if not quiet:
                print_good("Loading random listeers")
            if not hosts:
                temp = []
                number_hosts = random.choice(range(1, 20))
                for i in range(number_hosts):
                    temp.append(fake.ipv4())
                hosts = temp
            else:
                temp = []
                try:
                    number_hosts = len(hosts.split(","))
                except:
                    number_hosts = 1
                if number_hosts > 1:
                    for host in hosts.split(","):
                        temp.append(host)
                else:
                    temp = [ hosts ]
                hosts = temp
            if not port:
                port = get_random_port()
            if not host:
                host = all_interfaces
            name = "Http"
            uesr_agent = fake.user_agent()
            http_listener = Http_Listener(name, hosts, port, host, None, uesr_agent,
                                          default_headers, default_urls, "false", 
                                          None, None, None)
            listeners.Add_Http_Listener(http_listener)
            if not quiet:
                print_warn(f"""
    name:       {http_listener.name}
    port:       {http_listener.port}
    hosts:      {http_listener.hosts}
    bind:       {http_listener.host_bind}
    rotation:   {http_listener.host_rotation}
    user agent: {http_listener.user_agent}
    headers:    {http_listener.headers}
    urls:       {http_listener.urls}
    secure:     {http_listener.secure}
    cert:       None
    proxy:      None
    response:   {http_listener.reponse}
""")
            name = "Agent Listener - HTTP/s"
            uesr_agent = fake.user_agent()
            https_listener = Http_Listener(name, hosts, "443", host, None, uesr_agent,
                                          default_headers, default_urls, "true", 
                                          None, None, None)
            listeners.Add_Http_Listener(https_listener)
            if not quiet:
                print_warn(f"""
    name:       {https_listener.name}
    port:       {https_listener.port}
    hosts:      {https_listener.hosts}
    bind:       {https_listener.host_bind}
    rotation:   {https_listener.host_rotation}
    user agent: {https_listener.user_agent}
    headers:    {https_listener.headers}
    urls:       {https_listener.urls}
    secure:     {https_listener.secure}
    cert:       None
    proxy:      None
    response:   {https_listener.reponse}
""")
            smb_listener = Smb_Listener("Pivot - Smb")
            listeners.Add_Smb_Listener(smb_listener)
            if not quiet:
                print_warn(f"""
    name:       {smb_listener.name}
    namepipe:   {smb_listener.pipename}
""")
        else:
            for listener in listeners_block:
                for listener_type in listener.keys():
                    listener_name = listener[listener_type].get("name")
                    if not listener_name:
                        listener_name = fake.user_name()
                    if not quiet:
                        print_good("Loading listener profile:")
                    if listener_type == "http":
                        if not quiet:
                            print_warn(f"Type: {listener_type}")
                        listener_hosts = listener[listener_type].get("hosts")
                        if not listener_hosts:
                            if not hosts:
                                temp = []
                                number_hosts = random.choice(range(1, 20))
                                for i in range(number_hosts):
                                    temp.append(fake.ipv4())
                                listener_hosts = temp
                            else:
                                temp = []
                                try:
                                    number_hosts = len(hosts.split(","))
                                except:
                                    number_hosts = 1
                                if number_hosts > 1:
                                    for host in hosts.split(","):
                                        temp.append(host)
                                else:
                                    temp = [ hosts ]

                                listener_hosts = temp
                        listener_bind = listener[listener_type].get("bind")
                        if not listener_bind:
                            listener_bind = all_interfaces
                        listener_port = listener[listener_type].get("port")
                        if not listener_port:
                            listener_port = get_random_port()
                        listener_rotation = listener[listener_type].get("rotation")
                        if not listener_rotation:
                            listener_rotation = random.choice([ "random", "round-robin" ])
                        listener_user_agent = listener[listener_type].get("user_agent")
                        if not listener_user_agent:
                            listener_user_agent = fake.user_agent()
                        listener_headers = listener[listener_type].get("headers")
                        if profile_headers and not listener_headers:
                            listener_headers = profile_headers
                        listener_urls = listener[listener_type].get("urls")
                        if profile_request and not listener_urls:
                            listener_urls = profile_request
                        listener_secure = listener[listener_type].get("secure")
                        if not listener_secure:
                            listener_secure = random.choice([ "true", "false" ])
                        listener_cert = listener[listener_type].get("cert")
                        if not listener_cert:
                            listener_cert = None
                        else:
                            listener_cert_cert = listener_cert.get("cert")
                            listener_cert_key  = listener_cert.get("key")
                            listener_cert = Cert(listener_cert_cert, listener_cert_key)
                        listener_proxy = listener[listener_type].get("proxy")
                        if not listener_proxy:
                            listener_proxy = None
                        else:
                            listener_proxy_host = listener_proxy.get("host")
                            listener_proxy_port = listener_proxy.get("port")
                            listener_proxy_user = listener_proxy.get("user")
                            listener_proxy_pass = listener_proxy.get("pass")
                            listener_proxy = Proxy(listener_proxy_host, listener_proxy_port, 
                                                   listener_proxy_user, listener_proxy_pass)
                        listener_response = listener[listener_type].get("response")
                        if profile_response and not listener_response:
                            listener_response = profile_response
                        response = Response(listener_response)
                        listeners.Add_Http_Listener(Http_Listener(listener_name, 
                                        listener_hosts, listener_port,
                                        listener_bind, listener_rotation,
                                        listener_user_agent, listener_headers,
                                        listener_urls, listener_secure,listener_cert,
                                        listener_proxy, response))
                        if not quiet:
                            print_warn(f"""
    name:       {listener_name}
    port:       {listener_port}
    hosts:      {listener_hosts}
    bind:       {listener_bind}
    rotation:   {listener_rotation}
    user agent: {listener_user_agent}
    headers:    {listener_headers}
    urls:       {listener_urls}
    secure:     {listener_secure}
    cert:       {listener_cert}
    proxy:      {listener_proxy}
    response:   {listener_response}
""")
                    elif listener_type == "smb":
                        if not quiet:
                            print_warn(f"Type: {listener_type}")
                        listener_pipename = listener[listener_type].get("pipename")
                        if not listener_pipename:
                            listener_pipename = generate_pipename(random.choice(default_pipenames))
                        if not quiet:
                            print_warn(f"Pipename: {listener_pipename}")
                        listeners.Add_Smb_Listener(Smb_Listener(listener_name, listener_pipename))
                    elif listener_type == "external":
                        if not quiet:
                            print_warn(f"Type: {listener_type}")
                        listener_endpoint = listener[listener_type].get("endpoint")
                        if not listener_endpoint:
                            listener_endpoint = None
                        if not quiet:
                            print_warn(f"Endpoint: {listener_endpoint}")
                        listeners.Add_External_Listener(External_Listener(listener_name, listener_endpoint))
                    else:
                        print_warn(f"Listener {listener_type} is not available")

        if not service_block:
            service = None
        else:
            print_good("Creating optional service block")
            service_endpoint = dict(service_block).get("endpoint")
            service_password = dict(service_block).get("password")
            if not service_endpoint:
                service_endpoint = None
                service_password = None
            else:
                if not service_password:
                    service_password = fake.password()
            if not service_endpoint and not service_password:
                service = None
            else:
                if not quiet:
                    print_warn(f"""Service:
    endpoint: {service_endpoint}
    password: {service_password}
                    """)
                service = Service(endpoint=service_endpoint, password=service_password)

        print_good("Creating a demon :)")
            
        if not demon_block:
            injection = Injection(None, None, arch)
            sleep = random.choice(range(12, 60))
            jitter = random.choice(range(5, 70))
            demon = Demon(sleep=sleep, jitter=jitter, injection=injection)
            if not quiet:
                print("")
                print_warn(f"""Demon:
    sleep:    {sleep}
    jitter:   {jitter}
    spawn32:  {injection.spawn_x86}
    spawn64:  {injection.spawn_x64}
            """)
        else:
            demon_sleep = dict(demon_block).get("sleep")
            if not demon_sleep:
                demon_sleep = random.choice(range(12, 60))
            demon_jitter = dict(demon_block).get("jitter")
            if not demon_jitter:
                demon_jitter = random.choice(range(5, 70))
            demon_spawn32 = dict(demon_block).get("injection")["spawn32"]
            if not demon_spawn32:
                demon_spawn32 = None
            demon_spawn64 = dict(demon_block).get("injection")["spawn64"]
            if not demon_spawn64:
                demon_spawn64 = None
            demon_injection = Injection(spawn_x64=demon_spawn64,
                                        spawn_x86=demon_spawn32,
                                        arch=arch)
            if not quiet:
                print_warn(f"""Demon:
    sleep:    {demon_sleep}
    jitter:   {demon_jitter}
    spawn32:  {demon_injection.spawn_x86}
    spawn64:  {demon_injection.spawn_x64}
            """)
            demon = Demon(demon_sleep, demon_jitter, demon_injection)
        
        self.generator = Generator(teamserver=teamserver, 
                                   operators=operators, 
                                   listeners=listeners, 
                                   demon=demon,
                                   service=service)
        if self.generator:
            print_good("Generator complete")
        else:
            print_fail("Generator failed to compile :(")

    def Print(self) -> dict:
        return self.generator.Print()
    
    def Get(self) -> object:
        return self.generator
    
class Writer(Base):
    def __init__(self, filename = None) -> None:
        self.filename = filename

    def Write(self, profile) -> None:

        teamserver = profile["Teamserver"]
        operators  = profile["Operators"]
        listeners  = profile["Listeners"]
        service    = profile.get("Service")
        demon      = profile["Demon"]

        teamserver_host = teamserver["Host"]
        teamserver_port = teamserver["Port"]
        
        build = teamserver["Build"]
        build_compiler64 = build["Compiler64"]
        build_compiler86 = build["Compiler86"]
        build_assembler  = build["Nasm"]

        teamserver_block = f"""Teamserver {{
    Host = "{teamserver_host}"
    Port = "{teamserver_port}"

    Build {{
        Compiler64 = "{build_compiler64}"
        Compiler86 = "{build_compiler86}"
        Nasm = "{build_assembler}"
    }}
}}
"""
        operator_block = "Operators {"
        for operator in operators:
            operator_user = operator
            operator_pass = operators[operator_user]["Password"]
            operator_block += f"""
    user "{operator_user}" {{
        Password = "{operator_pass}"
    }}
"""
        operator_block += "}\n"

        listener_block = "Listeners {"
        for listener in listeners:
            for listener_type in listener.keys():
                listener_name = listener[listener_type].get("Name")

                if listener_type == "Http":
                    listener_port = listener[listener_type].get("Port")
                    listener_hosts = listener[listener_type].get("Hosts")
                    listener_bind  = listener[listener_type].get("HostBind")
                    listener_rotation = listener[listener_type].get("HostRotation")
                    listener_user_agent = listener[listener_type].get("UserAgent")
                    listener_secure = listener[listener_type].get("Secure")
                    listener_headers = listener[listener_type].get("Headers")
                    listener_urls = listener[listener_type].get("Urls")
                    listener_cert = listener[listener_type].get("Cert")
                    listener_proxy = listener[listener_type].get("Proxy")
                    listener_response = listener[listener_type].get("Response")
                    listener_response = listener_response.get("Headers")
                    listener_block += f'''
    {listener_type} {{
        Name         = "{listener_name}"
        Port         = {listener_port}
        Hosts        = {listener_hosts}
        HostBind     = "{listener_bind}"
        HostRotation = "{listener_rotation}"
        Secure       = {listener_secure}
        UserAgent    = "{listener_user_agent}"
        Uris         = {listener_urls}
        Headers      = {listener_headers}
'''
                    if listener_cert:
                        listener_block += f'''
        Cert {{
            Cert = "{listener_cert["Cert"]}"
            Key = "{listener_cert["Key"]}"
        }}
'''
                    if listener_proxy:
                        listener_block += f'''
        Proxy {{
            Host = "{listener_proxy["Host"]}"
            Port = {listener_proxy["Port"]}
            Username = "{listener_proxy["Username"]}"
            Password = "{listener_proxy["Password"]}"
        }}
'''
                    listener_block += f'''
        Response {{
            Headers  = {listener_response}
        }}
    }}
'''
                elif listener_type == "Smb":
                    listener_smb_pipename = listener[listener_type].get("Pipename")
                    listener_block += f'''
    Smb {{
        Name     = "{listener_name}"
        PipeName = "{listener_smb_pipename}"
    }}
'''
                elif listener_type == "External":
                    listener_ext_endpoint = listener[listener_type].get("Endpoint")
                    listener_block += f'''
    External {{
        Name      = "{listener_name}"
        Endpoint  = "{listener_ext_endpoint}"
    }}
'''
        listener_block += "}\n"

        if service:
            service_endpoint = service["Endpoint"]
            service_password = service["Password"]

            if service_endpoint and service_password:
                service_block = f"""Service {{
    Endpoint = "{service_endpoint}"
    Password = "{service_password}"
}}
"""
            else:
                service_block = None
        else:
            service_block = None

        demon_sleep = demon["Sleep"]
        demon_jitter = demon["Jitter"]
        demon_injection = demon["Injection"]
        injection_spawn64 = demon_injection["Spawn64"]
        injection_spawn32 = demon_injection["Spawn86"]

        demon_block = f"""Demon {{
    Sleep = {demon_sleep}
    Jitter = {demon_jitter}

    Injection {{
        Spawn64 = "{injection_spawn64}"
        Spawn32 = "{injection_spawn32}"
    }}
}}"""
        profile_block = teamserver_block + operator_block + listener_block
        if service_block:
            profile_block += service_block
        profile_block += demon_block
        profile_block = profile_block.replace("\'", "\"")
        
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(profile_block)
        else:
            print(profile_block)

if __name__ == "__main__":
    loaded_profiles = load_profiles()

    parser = argparse.ArgumentParser(
            prog='Deploy',
            description='Deploy\'s scripts to servers with fabric2\'s ssh or pypsrp winrm via threading')
    parser.add_argument('-c', '--config', type=argparse.FileType('r'), required=False, help='Config file to use, don\' use a conifg file for a completely random profile')
    parser.add_argument('-l', '--list', type=str_to_bool, nargs='?', const=True, default=False, help='List supported profiles')
    parser.add_argument('-s', '--sysnative', type=str_to_bool, nargs='?', const=True, default=False, help='Only support sysnative for spawn to')
    parser.add_argument('-a', '--arch', type=str, action='store', default="Nothing", help='Selected architecture between x86, x64 & x86_64')
    parser.add_argument('-p', '--profile', type=str, action='store', default="Nothing", help='Select a traffic profile')
    parser.add_argument('-H', '--host', type=str, action='store', default="Nothing", help='The listeners ip')
    parser.add_argument('-L', '--hosts', type=str, action='store', default="Nothing", help='The hosts array in the form of 10.0.0.1,10.0.0.2')
    parser.add_argument('-P', '--port', type=str, action='store', default="Nothing", help='Select a traffic profile')
    parser.add_argument('-o', '--outfile', type=str, action='store', default="Nothing", help='Output file of the final Havoc C2 pofile')
    parser.add_argument('-q', '--quiet', type=str_to_bool, nargs='?', const=True, default=False, help='Do not show banner')
    args = parser.parse_args()

    def list_profiles() -> None:
        for profile in loaded_profiles:
            print_good(f"Profile: {profile}")

    if args.list:
        list_profiles()
        sys.exit(0)

    template = None
    outfile = None
    config = None
    profile = None
    host = None
    hosts = None
    port = None
    arch = None

    if not args.quiet:
        print(f"{BANNER}")

    if args.profile != "Nothing":
        profile = args.profile
    else:
        profile = "any"
    
    if args.arch != "Nothing":
        arch = args.arch
    
    if args.host != "Nothing":
        host = args.host

    if args.hosts != "Nothing":
        hosts = args.hosts

    if args.port != "Nothing":
        port = args.port
    
    if args.outfile != "Nothing":
        outfile = args.outfile
    else:
        outfile = None

    if args.config:
        config = args.config.readlines()

    if args.sysnative:
        SYSNATIVE = True

    if not args.quiet:
        print_warn(f"""Selected options were:
    config:    {config is not None}
    outfile:   {outfile}
    profile:   {profile}
        """)
    
    generated_profile = Profile(quiet=args.quiet,
                                profiles=loaded_profiles,
                                profile=profile,
                                config=config,
                                host=host,
                                port=port,
                                hosts=hosts,
                                arch=arch)

    print_good(f"Saving profile to {outfile}")
    
    Writer(filename=outfile).Write(profile=generated_profile.Print())
