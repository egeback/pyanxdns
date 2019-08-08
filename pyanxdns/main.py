
# -*- coding: utf-8 -*-
import re
import sys

sys.path.insert(0,"../") # prefer local version
sys.path.insert(0,"./") # prefer local version
sys.path.append("../pyanxdns")
sys.path.append("./pyanxdns")

from pyanxdns.cli import CLI

if __name__ == '__main__':
    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(CLI().start())