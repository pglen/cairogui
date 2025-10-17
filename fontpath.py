import re
regex = re.compile(r'^\s*FontPath\s+(.*)\s*$', re.MULTILINE)

with open('/etc/xorg.conf') as f:
    data = f.read()
matches = regex.findall(data)

