import re

if '刷题' in '123刷题132':
    choice = re.search('[A-F]', '1231241C').group(0)
    print(choice)
