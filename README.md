# kukumail.py
m.kuku.lu wrapper in python
```py
import kukumail
c=kukumail.Client(session_hash="",proxy="https://localhost:8080")# Even without session_hash, it will work if you use c.register()
if c.me()=={}:
    print(c.register())
email=c.generate_random_email()#generate email
print(email)
print(c.recv_email(email))#List of emails sent
print(c.get_address())#List of emails
```
# star
Updates when the stars exceed 16
## What to update.
1. send a email
2. get list of available email domain
3. delete email address
4. async implementation
