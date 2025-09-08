import re

pat = re.compile(r'[A-Za-z]+')

match1 = pat.match('Hola mundo')

print(match1.group())  # Hola