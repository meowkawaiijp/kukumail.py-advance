# kukumail.py
m.kuku.lu wrapper in python
```py
import kukumail
c=kukumail.Client(requests.Session())
print(c.login("username","password"))# or c.register()
r=c.generate_random_email()#generate email
print(r)
print(c.recv_email(r))#List of emails sent
```
# star
Updates when the stars exceed 16
