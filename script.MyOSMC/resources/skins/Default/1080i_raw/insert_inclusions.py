from glob import glob
import os
from pprint import pprint
import re
import xml.etree.ElementTree as ET

cwd = os.getcwd()
dest_folder = cwd[:-4]

include_file = 'Includes.xml'
colours_file = 'defaults.xml'
control_file = 'ControlDefaults.xml'

fyles = glob('*.xml')

fyles.remove(include_file)
fyles.remove(colours_file)
fyles.remove(control_file)

def get_inclusion(child):

	return "".join([ ET.tostring(e) for e in child.getchildren() ] )


def process_Includes_file():
	tree = ET.parse(include_file)
	root = tree.getroot()

	inclusions = { child.attrib['name']: get_inclusion(child) for child in root}

	replacement_record = {}

	for fyle in fyles:

		new_fyle = os.path.join(dest_folder, fyle)

		with open(fyle, 'r') as f:

			replacement_record[fyle] = {}

			contents = ''.join(f.readlines())

			# number of times to run through the file replacing includes
			# this is essentially the max number of nesting we will allow
			for _ in range(5):
			
				for include_tag, guts in inclusions.iteritems():

					string = '<include>\s*' + include_tag + '.*</include>'

					contents, count =  re.subn(string, guts, contents, re.MULTILINE)
					
					replacement_record[fyle][include_tag] = count

		with open(new_fyle, 'w') as f:
			f.write(contents)

	pprint(replacement_record)


def process_colours_file():

	tree = ET.parse(colours_file)
	root = tree.getroot()

	colours = { child.attrib['name']: child.text for child in root}

	replacement_record = {}

	pprint(colours)

	for fyle in fyles:

		fyle = os.path.join(dest_folder, fyle)

		with open(fyle, 'r') as f:

			replacement_record[fyle] = {}

			contents = ''.join(f.readlines())

			for colour_name, colour_code in colours.iteritems():

				replacement_record[fyle][colour_name] = 0

				formats = [
						('>','</', '>','</'),
						('>\$VAR\[','\]</', '>','</'),
						('colordiffuse="$VAR[',']"', 'colordiffuse="','"'),
						('colordiffuse="','"','colordiffuse="','"')

				]

				for (left, right, repleft, repright) in formats:

					string = left + colour_name + right

					contents, count =  re.subn(string, repleft + colour_code + repright, contents, re.MULTILINE)
					
					replacement_record[fyle][colour_name] += count

		with open(fyle, 'w') as f:
			f.write(contents)

	pprint(replacement_record)


def insert_control_defaults():

	tree = ET.parse(control_file)
	root = tree.getroot()

	control_defaults = { child.attrib['type']: child.getchildren() for child in root}

	print control_defaults.keys()

	replacement_record = {}

	for fyle in fyles:

		fyle = os.path.join(dest_folder, fyle)	

		print fyle

		tree = ET.parse(fyle)

		for element in tree.getiterator():

			try:
				typ = element.attrib['type']
			except:
				continue

			existing_tags = [x.tag for x in element.getchildren()]

			default_lms = control_defaults.get(typ, [])

			for dlm in default_lms:
				if dlm.tag not in existing_tags:
					element.append(dlm)
		
		tree.write(fyle)

process_Includes_file()
insert_control_defaults()
process_colours_file()
