#!/usr/bin/python
import sys
import os
import shutil
import string
import stat
import re

COMMANDS=['init', 'new']
JOLT_SKEL='/home/mileswu/jolt-src/skel'
JOLT_GLOBAL='/home/mileswu/jolt-src/global'

JOLT_USER= os.environ['HOME'] + '/jolt2'

def provisionNewFile(path, filename):
	try:
		input_file = open(JOLT_SKEL + '/' + filename, 'r')
		output_file = open(path + '/' + filename, 'w')
	except:
		print("Some kind of IO error. Perhaps missing files in the skeleton?")
		sys.exit(1)

	for line in input_file:
		line = string.replace(line, '__JOLTDIR__', path)
		line = string.replace(line, '__PORT__', '1234')
		line = string.replace(line, '__USER__', os.environ['USER'])
		line = string.replace(line, '__RANDPW__', 'hi')
		output_file.write(line)
	
	input_file.close()
	output_file.close()

def runInit():
	if os.path.exists(JOLT_USER):
		print('You already have a jolt config set up at %s' % JOLT_USER)
		sys.exit(1)
	
	os.mkdir(JOLT_USER)
	provisionNewFile(JOLT_USER, 'monitrc')
	os.chmod(JOLT_USER + '/monitrc', stat.S_IWUSR | stat.S_IRUSR)
	home = os.environ['HOME']
	if os.path.lexists(home + '/.monitrc'):
		if os.path.realpath(home + '/.monitrc') != JOLT_USER + '/monitrc':
			print('For some reason you already have a .monitrc file in your home dir. Skipping creating the symbolic link. Without this done, your services may not start.')
			print('If you are sure you want to use jolt\'s configuration run:')
			print('  rm %s' % home + '/.monitrc')
			print('  ln -s %s %s' % (JOLT_USER + '/monitrc', home + '/.monitrc'))
	else:
		os.symlink(JOLT_USER + '/monitrc', home + '/.monitrc')
	os.system('monit')


if len(sys.argv) < 2:
	print('Usage: %s <command>' % sys.argv[0])
	print('where <command> is one of the following: %s' % ", ".join(COMMANDS))
	sys.exit(1)

if sys.argv[1] == 'init':
	runInit()

