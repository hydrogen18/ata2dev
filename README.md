ata2dev
-----

If you've ever had a hard drive fail on a linux system that has a non-trivial number of drives, you know how puzzling the output from `dmesg` can be.

```
[20573.128677] ata2.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x6 frozen
[20573.128740] ata2.00: failed command: FLUSH CACHE EXT
[20573.128769] ata2.00: cmd ea/00:00:00:00:00/00:00:00:00:00/a0 tag 0
[20573.128770]          res 40/00:01:00:00:00/00:00:00:00:00/40 Emask 0x4 (timeout)
[20573.128864] ata2.00: status: { DRDY }
[20573.128886] ata2: hard resetting link
[20583.117199] ata2: softreset failed (1st FIS failed)
[20583.117245] ata2: hard resetting link
[20593.101590] ata2: softreset failed (1st FIS failed)
[20593.101637] ata2: hard resetting link
[20628.051303] ata2: softreset failed (1st FIS failed)
[20628.051351] ata2: limiting SATA link speed to 1.5 Gbps
[20628.051355] ata2: hard resetting link
[20628.542512] ata2: SATA link up 1.5 Gbps (SStatus 113 SControl 310)
[20628.544288] ata2.00: configured for UDMA/133
[20628.544294] ata2.00: retrying FLUSH 0xea Emask 0x4
[20628.544495] ata2.00: device reported invalid CHS sector 0
[20628.544505] ata2: EH complete
```

The drive `ata2` is clearly broken, but what is that in the world of `/dev`? The number in `ata2` is the unique ID of the drive. This script maps those numbers to block devices. From there you can query using [smartmontools](http://sourceforge.net/apps/trac/smartmontools/wiki). In my case the output of the script looks like this:

```
ericu@katz:~/ata2dev$ python ata2dev.py 
/sys/block/sda -> host0 -> unique id: 1
/sys/block/sdb -> host1 -> unique id: 2
/sys/block/sdc -> host2 -> unique id: 3
/sys/block/sdd -> host3 -> unique id: 4
/sys/block/sde -> host4 -> unique id: 5
/sys/block/sdf -> host5 -> unique id: 6
/sys/block/sdg -> host11 -> unique id: 12
```

So querying using `smartctl -a /dev/sdb` gives me the drives serial number, which can be used to identify it for replacement
