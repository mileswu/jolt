#!/usr/bin/python
import sys
import os
import shutil
import string
import stat

COMMANDS=['init', 'new']
JOLT_SKEL='/home/mileswu/jolt-src/skel'
JOLT_GLOBAL='/home/mileswu/jolt-src/global'


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
	home = os.environ['HOME']
	path = home + '/jolt2'
	if os.path.exists(path):
		print('You already have a jolt config set up at %s' % path)
		sys.exit(1)
	
	os.mkdir(path)
	provisionNewFile(path, 'monitrc')
	os.chmod(path + '/monitrc', stat.S_IWUSR | stat.S_IRUSR)
	if os.path.lexists(home + '/.monitrc'):
		if os.path.realpath(home + '/.monitrc') != path + '/monitrc':
			print('For some reason you already have a .monitrc file in your home dir. Skipping creating the symbolic link. Without this done, your services may not start.')
			print('If you are sure you want to use jolt\'s configuration run:')
			print('  rm %s' % home + '/.monitrc')
			print('  ln -s %s %s' % (path + '/monitrc', home + '/.monitrc'))
	else:
		os.symlink(path + '/monitrc', home + '/.monitrc')

	os.system('monit')


if len(sys.argv) < 2:
	print('Usage: %s <command>' % sys.argv[0])
	print('where <command> is one of the following: %s' % ", ".join(COMMANDS))
	sys.exit(1)

if sys.argv[1] == 'init':
	runInit()

