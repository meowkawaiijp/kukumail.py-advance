# kukumail.py
m.kuku.lu wrapper in python
```py
import kukumail
c=kukumail.Client(proxy="https://localhost:8080")
print(c.login("username","password"))# or c.register()
r=c.generate_random_email()#generate email
print(r)
print(c.recv_email(r))#List of emails sent
```
# error
can't login
# star
Updates when the stars exceed 16
## What to update.
1. send a email
2. get list of available email domain
3. delete email address
4. async implementation
