import re

choice = re.search('[A-F]', '1231241C').group(0)
print(choice)
