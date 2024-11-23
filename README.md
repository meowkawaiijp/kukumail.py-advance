# kukumail.py
m.kuku.lu wrapper in python
```py
import kukumail
c=kukumail.Client(session_hash="",proxy="https://localhost:8080")# Even without session_hash, it will work if you use c.register()
if c.me()=={}:
    print(c.register())
r=c.generate_random_email()#generate email
print(r)
print(c.recv_email(r))#List of emails sent
```
# star
Updates when the stars exceed 16
## What to update.
1. send a email
2. get list of available email domain
3. delete email address
4. async implementation
