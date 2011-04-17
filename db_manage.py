#!/usr/bin/env python
from migrate.versioning.shell import main
main(url='postgresql://nags_dbuser:c0ns0le@localhost:5432/nags', debug='False', repository='database')
