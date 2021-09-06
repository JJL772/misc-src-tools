#!/usr/bin/env python3

"""

Documents game events

"""

import os
import sys
import argparse
import vdf 

parser = argparse.ArgumentParser(description='Parses GameEvents.res and ModEvents.res and generates Markdown documentation for them')
parser.add_argument('files', metavar='Resource files', type=str, nargs='+', help='List of .res files to parse for events')
parser.add_argument('-d --doc-file', type=str, dest='DOC_FILE', help='VDF (keyvalues) file that contains additional documentation to pin to each game event')
parser.add_argument('-o', required=True, type=str, dest='OUTPUT', help='Markdown output file')
args = parser.parse_args()

additional_docs = {}
output_stream = None

def document(file: dict):
	file = file[next(iter(file))] # Drop outer scope 
	for k, v in file.items():
		output_stream.write(f'## `{k}`\n\n')
		
		# Try to grab some of the additional documentation
		try:
			output_stream.write(additional_docs[k]['description'])
			output_stream.write('\n\n')
		except:
			pass
		
		if len(v.items()) == 0:
			continue
		output_stream.write(f'```c\n')
		# Enumerate params 
		for param, type in v.items():
			#output_stream.write(f'{type} {param}')
			# Try to grab more extra docs
			try:
				towrite = additional_docs[k]['params'][param]
				output_stream.write(f'{type:<7} {param:<20} // {towrite}\n')
			except:
				output_stream.write(f'{type:<7} {param:<20}\n')
		output_stream.write('```\n\n')

def main():
	# Open additional docs file 
	global additional_docs
	if args.DOC_FILE != None:
		try:
			with open(args.DOC_FILE, 'r') as fp:
				additional_docs = vdf.parse(fp)
				additional_docs = additional_docs[next(iter(additional_docs))] # VDF/KV is stupid- the outer scope is meaningless
		except:
			pass
		
	# Try to open output file
	global output_stream
	try:
		output_stream = open(args.OUTPUT, 'w')
	except:
		print(f'Failure while opening {args.OUTPUT} for writing')
		exit(1)
	
	# Open each passed file now, and document
	for f in args.files:
		with open(f, 'r') as fp:
			document(vdf.parse(fp))
			

if __name__ == "__main__":
	main()