import re

data = '''2020-01-17T02:44:31.526+01:00 <local3.notice> si0vm02571 event: SYSTEM: SYSTEM_AUTHENTICATION_SESSION_DENIED: - - Denied SEMP session 10.58.121.114 LDAP authentication for statspump (admin)'''


# pattern = re.compile(r'event.*:\s-').findall(data)
pattern = re.compile(r'S.*:').findall(data)
print(pattern)

# matches = pattern.finditer(data)

# for match in matches:
#     print(match)

# rex "event\s*(?<eventName>.+)\s*:"
