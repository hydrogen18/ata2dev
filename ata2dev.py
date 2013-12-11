import re
import os
import sys
if __name__ == "__main__":
	scsiHostDir = '/sys/class/scsi_host'
	hostDirPattern = re.compile('host(\d+)')
	uniqueIdFile = 'unique_id'
	sysBlockDir = '/sys/block'
	hostNumsToUniqueId = {}
	for hostDir in os.listdir(scsiHostDir):
		m = hostDirPattern.match(hostDir)
		if m == None:
			sys.stderr.write('Unparseable host directory: %s\n' % os.path.join(scsiHostDir,hostDir))
			continue
			
		hostNumber = int(m.group(1))
		
		with open(os.path.join(scsiHostDir,hostDir,uniqueIdFile)) as fin:
			uniqueId = int(fin.read())
		hostNumsToUniqueId[hostNumber] = uniqueId
		
	blockDeviceToHostNum = {}
	for blockSymLink in os.listdir(sysBlockDir):
		blockSymLink = os.path.join(sysBlockDir,blockSymLink)
		linkTarget = os.readlink(blockSymLink)
		hostNumber = None
		
		while hostNumber == None:
			head,tail = os.path.split(linkTarget)
			
			m = hostDirPattern.match(tail)
			
			if m !=None:
				hostNumber = int(m.group(1))
			elif len(head) == 0:
				hostNumber = -1
			else:
				linkTarget = head
		if hostNumber >= 0:
			blockDeviceToHostNum[blockSymLink] = hostNumber
		
	for blockSymLink, hostNumber in blockDeviceToHostNum.iteritems():
		if hostNumber in hostNumsToUniqueId:
			sys.stdout.write('%s -> host%i -> unique id: %i\n' % (blockSymLink,hostNumber, hostNumsToUniqueId[hostNumber],))
		
	
			
			
			
