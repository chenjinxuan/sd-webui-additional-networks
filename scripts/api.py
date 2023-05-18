from typing import Callable
from threading import Lock
from secrets import compare_digest
from modules import shared, script_callbacks

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from scripts import model_util


class Api:
    def __init__(self, app: FastAPI,  prefix: str = None) -> None:
        # if shared.cmd_opts.api_auth:
        #     self.credentials = dict()
        #     for auth in shared.cmd_opts.api_auth.split(","):
        #         user, password = auth.split(":")
        #         self.credentials[user] = password

        self.app = app
        self.prefix = prefix

        # self.add_api_route(
        #     'interrogate',
        #     self.endpoint_interrogate,
        #     methods=['POST'],
        #     response_model={}
        # )

        self.add_api_route(
            'refresh-model',
            self.endpoint_refesh_model,
            methods=['GET'],
            response_model={}
        )

    # def auth(self, creds: HTTPBasicCredentials = Depends(HTTPBasic())):
    #     if creds.username in self.credentials:
    #         if compare_digest(creds.password, self.credentials[creds.username]):
    #             return True
    #
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Incorrect username or password",
    #         headers={
    #             "WWW-Authenticate": "Basic"
    #         })

    def add_api_route(self, path: str, endpoint: Callable, **kwargs):
        if self.prefix:
            path = f'{self.prefix}/{path}'

        # if shared.cmd_opts.api_auth:
        #     return self.app.add_api_route(path, endpoint, dependencies=[Depends(self.auth)], **kwargs)
        return self.app.add_api_route(path, endpoint, **kwargs)

    # def endpoint_interrogate(self, req):
    #     print("11")
    #     return req
        # if req.image is None:
        #     raise HTTPException(404, 'Image not found')
        #
        # if req.model not in utils.interrogators.keys():
        #     raise HTTPException(404, 'Model not found')
        #
        # image = decode_base64_to_image(req.image)
        # interrogator = utils.interrogators[req.model]
        #
        # with self.queue_lock:
        #     ratings, tags = interrogator.interrogate(image)
        #
        # return models.TaggerInterrogateResponse(
        #     caption={
        #         **ratings,
        #         **interrogator.postprocess_tags(
        #             tags,
        #             req.threshold
        #         )
        #     })

    def endpoint_refesh_model(self):
        model_util.update_models()
        # return models.InterrogatorsResponse(
        #     models=list(utils.interrogators.keys())
        # )


def on_app_started(_, app: FastAPI):
    Api(app, '/an/v1')


script_callbacks.on_app_started(on_app_started)
