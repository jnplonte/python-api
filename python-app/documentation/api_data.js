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
    "name": "all",
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
    "filename": "app/v1/core/users/users.py",
    "groupTitle": "USERS"
  },
  {
    "type": "delete",
    "url": "/core/user/:id",
    "title": "delete user",
    "version": "1.0.0",
    "name": "delete",
    "group": "USERS",
    "permission": [
      {
        "name": "authenticated-user"
      }
    ],
    "description": "<p>delete user</p>",
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
            "type": "Boolean",
            "optional": false,
            "field": "force",
            "description": "<p>is force delete Ex. ?force=true</p>"
          }
        ]
      }
    },
    "filename": "app/v1/core/users/user.py",
    "groupTitle": "USERS"
  },
  {
    "type": "get",
    "url": "/core/user/:id",
    "title": "get user",
    "version": "1.0.0",
    "name": "get",
    "group": "USERS",
    "permission": [
      {
        "name": "authenticated-user"
      }
    ],
    "description": "<p>get user</p>",
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
    "filename": "app/v1/core/users/user.py",
    "groupTitle": "USERS"
  },
  {
    "type": "post",
    "url": "/core/users",
    "title": "insert user",
    "version": "1.0.0",
    "name": "post",
    "group": "USERS",
    "permission": [
      {
        "name": "authenticated-user"
      }
    ],
    "description": "<p>insert user</p>",
    "parameter": {
      "fields": {
        "body": [
          {
            "group": "body",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>user code</p>"
          },
          {
            "group": "body",
            "type": "String",
            "optional": false,
            "field": "firstName",
            "description": "<p>first name</p>"
          },
          {
            "group": "body",
            "type": "String",
            "optional": false,
            "field": "lastName",
            "description": "<p>last name</p>"
          },
          {
            "group": "body",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>unique email address</p>"
          },
          {
            "group": "body",
            "type": "String",
            "optional": false,
            "field": "phone",
            "description": "<p>unique phone number</p>"
          }
        ]
      }
    },
    "filename": "app/v1/core/users/users.py",
    "groupTitle": "USERS"
  },
  {
    "type": "put",
    "url": "/core/user/:id",
    "title": "update user",
    "version": "1.0.0",
    "name": "put",
    "group": "USERS",
    "permission": [
      {
        "name": "authenticated-user"
      }
    ],
    "description": "<p>update user</p>",
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
        "body": [
          {
            "group": "body",
            "type": "String",
            "optional": true,
            "field": "code",
            "description": "<p>user code</p>"
          },
          {
            "group": "body",
            "type": "String",
            "optional": true,
            "field": "firstName",
            "description": "<p>first name</p>"
          },
          {
            "group": "body",
            "type": "String",
            "optional": true,
            "field": "lastName",
            "description": "<p>last name</p>"
          },
          {
            "group": "body",
            "type": "String",
            "optional": true,
            "field": "email",
            "description": "<p>unique email address</p>"
          },
          {
            "group": "body",
            "type": "String",
            "optional": true,
            "field": "phone",
            "description": "<p>unique phone number</p>"
          },
          {
            "group": "body",
            "type": "Boolean",
            "optional": true,
            "field": "active",
            "description": "<p>is active user</p>"
          }
        ]
      }
    },
    "filename": "app/v1/core/users/user.py",
    "groupTitle": "USERS"
  }
] });
