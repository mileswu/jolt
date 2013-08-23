#!/usr/bin/python
import sys
import os
import shutil
import string
import stat
import re

JOLT_SKEL='/home/mileswu/jolt-src/skel'
JOLT_GLOBAL='/home/mileswu/jolt-src/global'
COMMANDS=['init', 'new', 'list']

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
	
	# Create empty provisioned file list as it's new
	saveProvisionedFile([])
	
	os.system('monit')
	
def loadProvisionedFile():
	try:
		provisioned_file = open(JOLT_USER + "/jolt.provisioned", 'r')
	except:
		print "Provisioned file not found"
		sys.exit(1)
		
	retval = []
	for line in provisioned_file:
		m = re.search('(\w+)\s+(\w+)', line)
		if m == None:
			print('Invalid entry in provisioned file (%s)' % line)
			print('Changes could be lost')
		retval.append({ 'service' : m.group(1), 'name': m.group(2) })
	
	return retval
	
def saveProvisionedFile(provisioned_services):
	try:
		provisioned_file = open(JOLT_USER + "/jolt.provisioned", 'w')
	except:
		print "Some IO error"
		sys.exit(1)
	
	for i in provisioned_services:
		provisioned_file.write("%s %s\n" % (i['service'], i['name']) )
	
	provisioned_file.close()
	
def runList():
	print('Available skeletons:')
	try:
		skels = os.listdir(JOLT_SKEL)
	except:
		print "Some IO error"
		sys.exit(1)
		
	filter_lambda = lambda filename: filename.endswith('.yml')
	map_lambda = lambda filename: filename[0:-4]
	skels = sorted(map(map_lambda, filter(filter_lambda, skels)))
	for i in skels:
		print('    %s' % i)
	
	print('Installed services:')
	provisioned_services = loadProvisionedFile()
	for i in provisioned_services:
		print('    %s - %s' % (i['service'], i['name']) )


if len(sys.argv) < 2:
	print('Usage: %s <command>' % sys.argv[0])
	print('where <command> is one of the following: %s' % ", ".join(COMMANDS))
	sys.exit(1)

if sys.argv[1] == 'init':
	runInit()
if sys.argv[1] == 'list':
	runList()

