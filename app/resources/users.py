import falcon
import app.services.serialization as json

from app.services.query import getQuery, getPassword
from app.models.users import Users


class UsersResources(object):
    def __init__(self, config, mongoConnection):
        self.config = config
        self.users = Users(mongoConnection)


    """
    @api {get} /users get all active user
    @apiVersion 1.0.0
    @apiName all
    @apiGroup USERS
    @apiPermission all
    @apiDescription get all active user
    
    @apiParam (url parameter) {String} [query] filter query <br/> Ex. `?query=firstName:johnpaul`
    @apiParam (url parameter) {Number} [limit=10] data limit <br/> Ex. `?limit=1`
    @apiParam (url parameter) {Number} [page=1] page number <br/> Ex. `?page=1`
    """

    """
    @api {get} /users/<id> get one user
    @apiVersion 1.0.0
    @apiName get
    @apiGroup USERS
    @apiPermission all
    @apiDescription get one user based on user id
    
    @apiParam (url segment) {String} id user id
    """
    def on_get(self, req, resp, id=None):
        if id is None:
            reqParams = getQuery(req.params)
            reqParams['active'] = True
            try:
                req.context['status'] = 'get'
                req.context['result'], req.context['pagination'] = self.users.getAll(reqParams, req.params)
            except Exception as e:
                req.context['statusCode'] = falcon.HTTP_400
                req.context['status'] = 'error'
                req.context['error'] = e
        else:
            try:
                req.context['status'] = 'get'
                req.context['result'] = self.users.getById(str(id))
            except Exception as e:
                req.context['statusCode'] = falcon.HTTP_400
                req.context['status'] = 'error'
                req.context['error'] = e

    """
    @api {post} /users insert one user
    @apiVersion 1.0.0
    @apiName post
    @apiGroup USERS
    @apiPermission all
    @apiDescription insert one user
    
    @apiParam (body) {String} firstName user first name
    @apiParam (body) {String} lastName user last name
    @apiParam (body) {String} email user email
    @apiParam (body) {String} userName user name
    @apiParam (body) {String} password user password
    @apiParam (body) {String} [phone] user contact number
    """
    def on_post(self, req, resp):
        if 'data' not in req.context or self.checkRequiredPostParameters(req.context['data']) is False:
            req.context['statusCode'] = falcon.HTTP_400
            req.context['status'] = 'data'
            req.context['error'] = [
                'firstName', 'lastName', 'email', 'userName', 'password'
            ]
            return

        req.context['data']['salt'], req.context['data']['password'] = getPassword(req.context['data']['password'])

        try:
            req.context['status'] = 'post'
            req.context['result'] = self.users.save(req.context['data'])
        except Exception as e:
            req.context['statusCode'] = falcon.HTTP_400
            req.context['status'] = 'error'
            req.context['error'] = e

    """
    @api {put} /users/<id> update one user
    @apiVersion 1.0.0
    @apiName put
    @apiGroup USERS
    @apiPermission all
    @apiDescription update one user based on user id
    
    @apiParam (url segment) {String} id user id
    @apiParam (body) {String} [firstName] user first name
    @apiParam (body) {String} [lastName] user last name
    @apiParam (body) {String} [email] user email
    @apiParam (body) {String} [userName] user name
    @apiParam (body) {String} [password] user password
    @apiParam (body) {String} [phone] user contact number
    """
    def on_put(self, req, resp, id=None):
        if id is None:
            return

        if 'password' in req.context['data']:
            req.context['data']['salt'], req.context['data']['password'] = getPassword(req.context['data']['password'])

        try:
            req.context['status'] = 'put'
            req.context['result'] = self.users.updateById(str(id), req.context['data'])
        except Exception as e:
            req.context['statusCode'] = falcon.HTTP_400
            req.context['status'] = 'error'
            req.context['error'] = e

    """
    @api {delete} /users/<id> delete one user
    @apiVersion 1.0.0
    @apiName delete
    @apiGroup USERS
    @apiPermission all
    @apiDescription delete one user based on user id
    
    @apiParam (url segment) {String} id user id
    """
    def on_delete(self, req, resp, id=None):
        if id is None:
            return

        try:
            req.context['status'] = 'delete'
            req.context['result'] = self.users.updateById(str(id), {'active': False})
        except Exception as e:
            req.context['statusCode'] = falcon.HTTP_400
            req.context['status'] = 'error'
            req.context['error'] = e

    def checkRequiredPostParameters(self, data):
        if 'firstName' not in data or 'lastName' not in data or 'email' not in data or 'userName' not in data or 'password' not in data:
            return False
        
        return True
