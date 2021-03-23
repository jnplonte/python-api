define({ "api": [
  {
    "type": "post",
    "url": "/auth/token",
    "title": "fetch user information",
    "version": "1.0.0",
    "name": "post-token",
    "group": "AUTHENTICATION",
    "permission": [
      {
        "name": "all"
      }
    ],
    "description": "<p>fetch user information via token</p>",
    "parameter": {
      "fields": {
        "body": [
          {
            "group": "body",
            "type": "String",
            "optional": false,
            "field": "key",
            "description": "<p>user key</p>"
          }
        ]
      }
    },
    "filename": "app/v1/authentication/token.py",
    "groupTitle": "AUTHENTICATION"
  },
  {
    "type": "get",
    "url": "/core/users",
    "title": "get all users",
    "version": "1.0.0",
    "name": "getAll",
    "group": "USERS",
    "permission": [
      {
        "name": "authenticated-user"
      }
    ],
    "description": "<p>get all users</p>",
    "parameter": {
      "fields": {
        "query": [
          {
            "group": "query",
            "type": "String",
            "optional": true,
            "field": "query",
            "description": "<p>query <br/> sample: <code>?query=test:abc</code></p>"
          },
          {
            "group": "query",
            "type": "Number",
            "optional": true,
            "field": "page",
            "description": "<p>page</p>"
          },
          {
            "group": "query",
            "type": "Number",
            "optional": true,
            "field": "limit",
            "description": "<p>limit</p>"
          }
        ]
      }
    },
    "filename": "app/v1/core/users.py",
    "groupTitle": "USERS"
  },
  {
    "type": "get",
    "url": "/core/user/:id",
    "title": "get one user",
    "version": "1.0.0",
    "name": "getOne",
    "group": "USERS",
    "permission": [
      {
        "name": "authenticated-user"
      }
    ],
    "description": "<p>get one users</p>",
    "parameter": {
      "fields": {
        "url segment": [
          {
            "group": "url segment",
            "type": "String",
            "optional": false,
            "field": "id",
            "description": "<p>user id</p>"
          }
        ],
        "url parameter": [
          {
            "group": "url parameter",
            "type": "String",
            "optional": false,
            "field": "key",
            "description": "<p>key search Ex. ?key=name</p>"
          }
        ]
      }
    },
    "filename": "app/v1/core/user.py",
    "groupTitle": "USERS"
  }
] });
