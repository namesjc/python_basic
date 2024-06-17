import re


text_to_search = '''
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890

Ha HaHa

MetaCharacters (Need to be excaped):
. ^ $ * + ? { } [ ] \ | ( )

coreyms.com

321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234

Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T

cat
mat
pat
bat

'''

sentence = 'Start a sentence and the bring it to the end'

# pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')
# pattern = re.compile(r'\d\d\d[-.]\d\d\d[-.]\d\d\d\d') # it only matched - and . with []
# pattern = re.compile(r'[89]00[-.]\d\d\d[-.]\d\d\d\d')  # only match 800 and 900
pattern = re.compile(r'[1-5]') # match numbers between 1 to 5
# pattern = re.compile(r'[a-zA-Z]') # match numbers between a to z or A to Z
# pattern = re.compile(r'[^b]at')  # rule out the first letter 'b' and matche the left two letters are 'at'
# pattern = re.compile(r'\d{3}.\d{3}.\d{4}') # {3} means matche the same 3 \d
# pattern = re.compile(r'(Mr|Ms|Mrs)\.?\s[A-Z]\w*')  # ? mean after Mr '.' is optional

# pattern = re.compile(r'[a-zA-Z0-9.-]+@[a-zA-Z-]+\.(com|edu|net)')

matches = pattern.finditer(text_to_search)

for match in matches:
    print(match)

# pattern = re.compile(r'\d{3}.\d{3}.\d{4}')
# with open('data.txt', 'r', encoding='utf-8') as f:
#     contents = f.read()
#     matches = pattern.finditer(contents)
#     for match in matches:
#         print(match)
