define({
  "name": "Python Api",
  "version": "1.0.0",
  "description": "Python Api Documentation",
  "title": "Python Api Documentation",
  "url": "https://www.jnpl.me/playground/pythonapi/<version>",
  "header": {
    "title": "GETTING STARTED",
    "content": "<p>all api that has a <strong>permision</strong> set to <strong>authenticated-user</strong> is required to have a <code>user-key</code> as a headers</p>\n<h3>API EXPECTED SUCCESS RESULTS</h3>\n<pre class=\"prettyprint\">{\n    \"status\": \"success\",\n    \"message\": \"<success-description>\",\n    \"executionTime\": 1.000,\n    \"data\": \" ... \",\n    ? \"pagination\": {\n        \"totalData\": 0,\n        \"totalPage\": 0,\n        \"currentPage\": 0\n    }\n}\n</code></pre>\n<h3>API EXPECTED FAILED RESULTS</h3>\n<pre class=\"prettyprint\">{\n    \"status\": \"failed\",\n    \"message\": \"<failed-description>\",\n    \"executionTime\": 0,\n    \"data\": \" ... \"\n}\n</code></pre>\n<h3>API STATUS</h3>\n<ul>\n<li><code>200</code> =&gt; status is success</li>\n<li><code>204</code> =&gt; status is success but no data to be shown</li>\n<li><code>400</code> =&gt; status is failed</li>\n<li><code>401</code> =&gt; status is failed and invalid x-python-api-key</li>\n<li><code>403</code> =&gt; status is failed and user is not authorized to access the api endpoint</li>\n<li><code>404</code> =&gt; api endpoint dosen't exists</li>\n<li><code>405</code> =&gt; no method is available for that particular api endpoint</li>\n<li><code>500</code> =&gt; internal server error</li>\n</ul>\n"
  },
  "template": {
    "withCompare": false,
    "withGenerator": false
  },
  "sampleUrl": null,
  "defaultVersion": "0.0.0",
  "apidoc": "0.3.0",
  "generator": {
    "name": "apidoc",
    "time": "2021-03-24T00:52:19.112Z",
    "url": "https://apidocjs.com",
    "version": "0.27.1"
  }
});
