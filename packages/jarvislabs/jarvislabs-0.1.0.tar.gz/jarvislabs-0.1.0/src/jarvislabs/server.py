from pydantic import BaseModel, create_model
from fastapi import FastAPI
from jltest import App
from typing import Callable, Any
import uvicorn
import inspect
import asyncio

class Server:
    def __init__(self, app: App):
        self.app = app
        self.fastapi_app = FastAPI()
        self._setup()
        self._setup_routes()

    def _setup(self):
        if self.app.setup_fn:
            self.app.setup_fn()

    def _setup_routes(self):
        for name, method in self.app.api_endpoints.items():
            print(f"Route name {name}")
            self._create_route(method)

    def _create_route(self, method: Callable):
        method_name = method.__name__
        signature = inspect.signature(method)
        parameters = signature.parameters

        pydantic_model = None
        for param in parameters.values():
            if inspect.isclass(param.annotation) and issubclass(param.annotation, BaseModel):
                pydantic_model = param.annotation
                break

        if pydantic_model:
            @self.fastapi_app.post(f"/{method_name}")
            async def endpoint(body: pydantic_model):
                result = await self.app.api_endpoints[method_name](body)
                return result
        else:
            # Create a Pydantic model for the request body
            fields = {}
            for name, param in parameters.items():
                if name == 'self':
                    continue
                annotation = param.annotation if param.annotation != inspect.Parameter.empty else Any
                default = ... if param.default == inspect.Parameter.empty else param.default
                fields[name] = (annotation, default)

            DynamicModel = create_model(f'{method_name.capitalize()}Body', **fields)

            @self.fastapi_app.post(f"/{method_name}")
            async def endpoint(body: DynamicModel):
                kwargs = body.dict()
                result = await self.app.api_endpoints[method_name](**kwargs)
                return result

    def run(self, host: str = "0.0.0.0", port: int = 6006):
        @self.fastapi_app.get("/health")
        async def health():
            return {"success": True}
        uvicorn.run(self.fastapi_app, host=host, port=port)