# Socketwebserver
An module for creating web servers, using only python built-in libraries
# Installing
To install this.\
You need to `git clone` the reposity\
then go to the folder, you cloned into\
and type `pip install .`
# How to use
To use this,\
you first need to import it with this line:
```python
import sockwebserver as s
```
Then, define a callback.
```python
def mypage(path,method,params):
  print('some visited me!')
  return "Hello!" # Always must return an HTML string.
```
And add rule.
```python
s.addrule('/',mypage)
```
And then start it!
```python
s.start()
```
Actually simple. Right?\
If you want to load up special test page, use this:
```python
s.test()
```
