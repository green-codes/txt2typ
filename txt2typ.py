#!python3

import sys
import re
import argparse

supported_modes = ['D','d','S','s']
default_mode = 's'

# process command arguments
parser = argparse.ArgumentParser()
parser.add_argument("src_file", help="Input text file")
parser.add_argument("dest_file", help="Output gtypist file")
parser.add_argument("-m", "--mode", help="Type of typing exercise, supported: [D,d,S,s]; see GNU Typist Manual.")
parser.add_argument("-a", "--alt", help="Alternative mode, disables soft wrapping and treats each line in the input file as one line in the typing exercise. Default mode treats each line as a paragraph.", action="store_true")
args = parser.parse_args()
mode = default_mode if args.mode==None else args.mode
if mode not in supported_modes:
  raise Exception("Mode not supported: {}".format(mode))

row_limit = 20 if mode in ['S','s'] else 10
col_limit = 78

# preprocess input file; replace non-ascii chars with space
with open(args.src_file, 'r') as f:
  lines = f.readlines()
  lines = [re.sub(r'[^\x00-\x7f]', r' ', line) for line in lines]

# alt mode: input file already soft wrapped, make one big section  
if args.alt:
  sections = [[]]
  for line in lines:
    if len(line.strip())==0: continue
    sections[-1] += [line.strip().split(' ')]

# default mode: treats each line as a paragraph/section
else:
  # parse lines and soft wrap
  sections = []  # each line in original file is a section
  for line in lines:
    if len(line.strip())==0: continue  # skip empty line in original file
    words = line.strip().split(' ')  # break out each word
    section = [[]]  # each section contains multiple soft-wrapped lines
    for word in words:
      curr_line_len = sum([len(word)+1 for word in section[-1]])
      if curr_line_len + len(word) >= col_limit:
        section += [[]]  # new line if adding curr word exceeds col_limit
      section[-1] += [word]
    sections += [section]

# write sections to file
with open(args.dest_file, 'w') as f:
  for i,section in enumerate(sections):
    f.write("*:{}\n".format(i))
    j = 0
    for line in section:
      if j >= row_limit: j = 0  # new page if exceeding row_limit
      f.write("{}:".format(mode if j==0 else ' '))
      f.write(" ".join(line) + "\n")
      j += 1
