import requests
import json
import time

pintoken = "iBg10iO7itdSHK7dW2nv1w+oE+XS9dj9EtLtUo7EPDzK/7fUJCA3OCPLMRjoVF9Z+YBNJe8X1bHOkV3Asv24x1gCJSIBE0flm6heQfOcupsNk4arOdvbVhmf5hRkqItUWmsBwR67b4wH5gkwaoxmFgPd7lvd7jdyW9jIn6rUBx4="
private_key='''-----BEGIN RSA PRIVATE KEY-----\r\nMIICWwIBAAKBgQCW6rohnxwLm1MS+ouvZx4W2f5j4GnjvsYlgXlr+cHSso238Q9A\r\n/2MkyNW/U0iYnRK47urxQyAd6EEgkT3v2cHOKqQMjCKR3RLTlzsqBLWLMyWJEXnc\r\nhJMMig2DO3pFVa9ezII/jUd8m/33PLs2w2uunlFDP/KIL0xptWwoIDvv1QIDAQAB\r\nAoGAC84fsjqWgIftZyonHBjmXyY9QoXO8qw9JrjqjRoz4a3q7Q0TwuNXV4zIP5ed\r\nsaZzzPiPc0DrdbtxwMDrxePUR5QDT2QSk/jdEw8mIN4Z1fPQe1Tw83eifgKOzcgP\r\nOdo4pOw8tSjrKx6CRuWhejjcPt2QbnvwF6M6u0vI9EklUdECQQC9MSJBXkD0jz5E\r\nu8rEixbp9z0KAhtNNOytgW66eM8MQsrK5qLiPN1DFPxctaITpWxv/ItutQnvPumT\r\n8wQ0d2+9AkEAzDWMRG0sqD5Gb60WlNkhO9nfMjlwPWMV/xzUUTdMUVbZOW4zJVHh\r\nTgEN2wjPHtwrXpRvSnuCunqV88TKbfjV+QJAGCpVeMoEO/ir+HWQMcieVaYp2sRo\r\nHlV7QbI9pX3W3HcPlhkdhw5FKNNeZK0ilaXUkv1MBgkDytZbWXV5/QWgdQJAYamu\r\nZr9L3z7BUwGVziQ117jwHMYJnuI3j+XKyPjIYBJIG0ZP4aZSOYsZhEqnO9wSRc55\r\nl0aQk/yyoH3aTlP2iQJALZhoLRDINOVyijl46izDC46uaIwxHDxs522DH/fBobje\r\nbvuw7LSwj9YZjvcMXtQxmalJdlPOUL1CjLdFmNQ5Fw==\r\n-----END RSA PRIVATE KEY-----\r\n'''
sessionid='224e5a92-d313-467a-ab34-49d13b5ccbd3'
userid='a935fb65-3ac0-3a2b-b5ff-79b8848c3659'






# r = requests.post('http://127.0.0.1:5000/api/v1/pub/',json={'id':'id', 'trace':'trace333', 'data':'data','time':time.time()})
# print(r)
# print(r.json())
#
r = requests.post('http://127.0.0.1:5000/api/v1/pub/',json={'userid':userid, 'data':'dfkjsofjf', 'pintoken': pintoken, 'private_key':private_key, 'pin':'000000', 'sessionid': sessionid})
print(r)
print(r.json())


# r = requests.get('http://127.0.0.1:5000/api/v1/creat_id/')
# # print(r)
# print(r.json())


# r = requests.post('http://127.0.0.1:5000/api/v1/charge/',json={'userid':userid, 'amount':'23',})
# print(r)
# print(r.json())


