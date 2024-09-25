# httpc

**httpx with CSS**

## Installation

```console
pip install -U httpc
```

## Examples

```python
>>> import httpc
>>> response = httpc.get("https://www.python.org/")
>>> response.match("strong")  # CSS Matching
[<Node strong>, <Node strong>, <Node strong>]
>>> response.match("strong").bc.text()  # Broadcasting
['Notice:', 'A A', 'relaunched community-run job board']
>>> response.single("div")  # .single() method
ValueError: Query 'div' matched with 47 nodes (error from 'https://www.python.org/').
>>> response.single("div", remain_ok=True)  # .single() method
<Node div>
>>> response.single("#content")
<Node div>
>>> httpc.get("https://python.org")
<Response [301 Moved Permanently]>
>>> httpc.common.get("https://python.org")  # ClientOptions and httpc.common
<Response [200 OK]>
>>> httpc.common.get("https://hypothetical-unstable-website.com/", retry=5)  # retry parameter
Attempting fetch again...
Attempting fetch again...
Successfully retrieve 'https://hypothetical-unstable-website.com/'
<Response [200 OK]>
>>> httpc.get("https://httpbin.org/status/400")
<Response [400 BAD REQUEST]>
>>> httpc.get("https://httpbin.org/status/400", raise_for_status=True)  # raise_for_status as parameter
httpx.HTTPStatusError: Client error '400 BAD REQUEST' for url 'https://httpbin.org/status/400'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
```

## Release Note

* 0.3.0: Add `new` parameter, remove `select` method, rename `css` to `match` from CSSTool, remove cache_api.py (unused script), add url note, retry if server error on raise_for_status, bugfix
* 0.2.0: Initial release
