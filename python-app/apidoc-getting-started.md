all api that has a **permision** set to **authenticated-user** is required to have a `user-key` as a headers

### API EXPECTED SUCCESS RESULTS

```
{
    "status": "success",
    "message": "<success-description>",
    "executionTime": 1.000,
    "data": " ... ",
    ? "pagination": {
        "totalData": 0,
        "totalPage": 0,
        "currentPage": 0
    }
}
```

### API EXPECTED FAILED RESULTS

```
{
    "status": "failed",
    "message": "<failed-description>",
    "executionTime": 0,
    "data": " ... "
}
```

### API STATUS

- `200` => status is success
- `204` => status is success but no data to be shown
- `400` => status is failed
- `401` => status is failed and invalid x-python-api-key
- `403` => status is failed and user is not authorized to access the api endpoint
- `404` => api endpoint dosen't exists
- `405` => no method is available for that particular api endpoint
- `500` => internal server error
