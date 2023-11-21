"""
The socket-server source code.
"""
import socket,traceback,mimetypes
import os.path
from urllib.parse import urlparse, parse_qs
__version__ = '0.1'
paths = {}
errorstyle = """<style>
* {
    font-family: Helvetica;
}
p {
    line-height: 0.2;
    /*margin:-10px 0 -10px 0;*/
    color: white;
}
body {
    background-color: #171b22;
}
h1 {
    color: white;
    border-bottom: 2px solid white;
    padding: 10px;
}
pre {
    color: #ff2667;
    background-color: black;
    border-radius: 20px;
    padding: 10px;
}
</style>""" # An error style, for error pages
modrenstyle = """<style>
* {
    font-family: Helvetica;
}
p {
    line-height: 0.2;
    /*margin:-10px 0 -10px 0;*/
    color: white;
}
span {
    color: white;
}
ui, ul, ol {
    color: white;
}
body {
    background-color: #171b22;
}
h1, h2, h3, h4, h5 {
    color: white;
    border-bottom: 2px solid white;
    padding: 10px;
}
pre {
    color: white;
    background-color: black;
    border-radius: 20px;
    padding: 10px;
}
code {
    color: #ffff96;
    background-color: black;
    border-radius: 5px;
}
button {
    background-color: #454545;
    border-radius: 5px;
    color: white;
    border: none;
    cursor: pointer;
    transition-duration: 0.5s;
}
button:hover {
    background-color: #626262;
}
button:active {
    background-color: #1d1d1d !important;
}
#alphalist {
    list-style-type:lower-alpha;
}
#error {
    color: #ff2667;
}
a, a:hover, a:active, a:visited { color: white; }
</style>""" # Modern style. Dark theme and better fonts.
def addrule(path,callback): # Add a rule to the rules dict.
    """
    Add an new path for your server.
    You can make it by using this function.
    The arguments you need to provide are
    (path, callback)
    Yea, pretty simple, right?
    To make a callback function, there's should be those
    arguments for function:
    (path, method, params)
    The path argument is basically where user goes to.
    It could be like /api/v1/access/user
    And method could be the one of GET, POST, HEAD, PUT, DELETE, etc.
    And the params... Are just query params (dict eg. like {"a": ["b"]})
    And by the way, you need to return an html in callback function.
    And also, if you gonna add an callback to existing path which has other callback,
    it just overwrites the callback.
    """
    paths[path] = callback
    return
def start(host='localhost',port=8000,debug=False,acesspaths=False): # Start the server.
    """
    Runs the server itself.
    """
    print("Creating server..")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f'Sucessfully created a server on computer "{socket.gethostname()}"!')
    print(f'You may see the web page at {host}:{port}')
    while 1: 
        csock, caddr = server.accept()
        cfile = csock.makefile('rwb')
        print(f"Got connection from {caddr}!")
        line = cfile.readline().decode().strip()
        try:
            method, path, _ = line.split(' ')
        except:
            continue
        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)
        path = path.split('?')[0]
        if debug:
            print(f'Requested path: {path}\nMethod: {method}\nParams: {query_params}')
        if path in paths:
            try:
                resp = paths[path](method=method, path=path, params=query_params)
                response = f"""HTTP/1.0 200 OK
Content-Type: text/html

{resp}
""".replace('modern.style',modrenstyle,1)
                cfile.write(response.encode())
                cfile.flush()
                cfile.close()
                csock.close()
            except:
                response = f"""HTTP/1.0 500 Internal Server Error
Content-Type: text/html


<html>
<head>
<title>Socket-server</title>
{errorstyle}
</head>
<body>
<h1>Internal Server Error</h1>
<p>There was an error in the server.</p>
<p>The error logs are:</p>
<pre>{traceback.format_exc()}</pre>
<p>If you are seeing this not for first time, Tell the owner of site to repair the issue</p>

</body>
</html>
"""
                cfile.write(response.encode())
                cfile.flush()
                cfile.close()
                csock.close()
        else:
            if os.path.isfile(path[1:]) and acesspaths:
                mt = mimetypes.guess_type(path[1:])
                if mt:
                    with open(path[1:],'rb') as f:
                        cfile.write(f"HTTP/1.0 200 OK\nContent-Type: {mt}\n\n".encode())
                        cfile.write(f.read())
                        cfile.flush()
                        cfile.close()
                        csock.close()
                        
                        
            else:
                response = f"""HTTP/1.0 404 Not Found
Content-Type: text/html

<html>
<head>
<title>Socket-server</title>
{errorstyle}
</head>
<body>
<h1>Not found</h1>
<p>The page you are looking at, doesnt exist.</p>
</body>
</html>
"""
                cfile.write(response.encode())
                cfile.flush()
                cfile.close()
                csock.close()
def test(): # An function, to load up testing page
    addrule('/',mainpage)
    addrule('/error',errortest)
    addrule('/params',paramstest)
    addrule('/method',methodtest)
    addrule('/path',pathtest)
    addrule('/modernstyle',modernpage)
    start(acesspaths=True,debug=True)
def errortest(path,method,params):
    raise Exception("Whoops! I am a really long error message cause i dont know, maybe thats cause i am really really useless to read.....")
def paramstest(path,method,params):
    return f"Your params are: {params}"
def methodtest(path,method,params):
    return f"Your method is: {method}<br>Use something like postman to see other methods"
def pathtest(path,method,params):
    return f"Your path is: {path}"
def aboutpage(path,method,params):
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>About Socket-Server</title>
{modrenstyle}
</head>
<body>
<div class="container">
    <h1>About Socket-Server</h1>
    <p>The Socket-Server is a simple server implementation that allows you to define custom paths and callbacks for handling HTTP requests. It provides a basic framework for creating a server and handling different routes.</p>
<h2>Features</h2>
<ul>
    <li>Define custom paths and callbacks for your server.</li>
    <li>Supports various HTTP methods like GET, POST, HEAD, PUT, DELETE, etc.</li>
    <li>Retrieve query parameters from the URL.</li>
    <li>Handles errors and displays error messages.</li>
</ul>

<h2>Usage</h2>
<p>To use the Socket-Server, follow these steps:</p>
<ol>
    <li>Import the server module:</li>
</ol>
<pre>import server</pre>
<ol start="2">
<li>Define the paths and callbacks using the <code>server.addrule()</code> function:</li>
</ol>
<pre>def mainpage(path,method,params):
    return "Hello, World!"
server.addrule('/', mainpage)
</pre>
<p>The <code>addrule()</code> function allows you to specify a path and the corresponding callback function that will handle the request for that path.</p>
<ol start="3">
<li>Start the server using the <code>server.start()</code> function:</li>
</ol>
<pre>server.start()</pre>
<p>The <code>server.start()</code> function creates a server socket, binds it to a host and port, and starts listening for incoming connections. It then handles each request by calling the appropriate callback function based on the requested path.</p>
<h2>Example</h2>
<p>Here's an example of how you can use the Socket-Server:</p>
<pre>import server
def mainpage(path,method,params):
    return "Hello, World!"
server.addrule('/', mainpage)
server.addrule('/', mainpage)
server.start()</pre>
<h2>Additional Information</h2>
<ul>
    <li>The server runs on the localhost by default, but you can specify a different host and port if needed.</li>
    <li>The server supports basic error handling and displays error messages when an exception occurs.</li>
    <li>The server provides a default main page that can be used for testing purposes.</li>
</ul>

<p>If you have any further questions, feel free to ask!</p>
</div>
</body>
</html>
"""
def modernpage(path,method,params):
    return """
<html>
<head>
<title>Socket-server</title>
modern.style
</head>
<body>
<h1>Modern style</h1>
<p>Modern style is a tiny addon for your web-page</p>
<p>If you want to make your pages look modern</p>
<p>With a dark theme.</p>
<h2>Adding to web-page</h2>
<p>You can add it easily.</p>
<p>Just add <code>modern.style</code> into your head tag.</p>
<p>And please, dont put it into other web-pages that dont use socket-server</p>
<p>cause the server replaces <code>modern.style</code> with an style tag.</p>
<h2>Example</h2>
<button>A button.</button><br>
<ol>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
</ol>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</ul>
<ol>
    <li id="alphalist">alphalist id</li>
    <li id="alphalist">alphalist id</li>
    <li id="alphalist">alphalist id</li>
</ol>
<pre>
print("Some code.")
</pre>
<pre id="error">
An error. You can make it by setting error id into pre tag or code tag
And also, it could be seen in error pages like Internal server error
</pre>
<code>Inline code.</code><br>
<code id="error">Inline error.</code>
<h1>H1</h1>
<h2>H2</h2>
<h3>H3</h3>
<h4>H4</h4>
<h5>H5</h5>
<p>An paragraph.</p>
<span>Span element.</span>
</body>
</html>
"""
def mainpage(path,method,params):
    return f"""
<html>
<head>
<title>Socket-server testing page</title>
{modrenstyle}
</head>
<body>
<h1>Socket-server testing page</h1>
<p>In this page, you can test the socket-server server.</p>
<p>The error page, not found page, etc.</p>
<p>The tests are:</p>
<a href="doesntexist">Non-existing page/404 page</a><br>
<a href="error">Server error page</a><br>
<a href="params">Getting params page</a><br>
<a href="path">Getting path page</a><br>
<a href="method">Getting method page</a><br>
<a href="cat.jpg">Getting a file from server</a><br>
<a href="text.txt">An text file</a>
<p>Other pages:</p>
<a href="about">About socket-server</a><br>
<a href="modernstyle">Modern style</a>
<h2>About this page</h2>
<p>Normally, this page is used to test the functions of socket-server</p>
<p>But also, its used as default page for server</p>
<p>when the server doesnt import in other script,</p>
<p>but runs with python.</p>
<p>Or when test() function was used in code.</p>

</body>
</html>
"""
if __name__ == '__main__': # Check if script is running as main
    test()
