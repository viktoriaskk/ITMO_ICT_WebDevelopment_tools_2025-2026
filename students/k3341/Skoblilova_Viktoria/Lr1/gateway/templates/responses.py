"""
Шаблоны описаний ответов OpenAPI и хелперы JSONResponse для единообразных ошибок.
"""

from dataclasses import dataclass
from fastapi.responses import JSONResponse


@dataclass
class TemplatesResponsesDataclass:
    template_200 = {
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "examples": {
                        "example": {
                            "summary": "Template Value",
                            "value": {
                                "status": "success",
                                "result": "Any",
                            },
                        },
                    },
                },
            },
        }
    }
    template_207 = {
        207: {
            "description": "Multi-status (for redirect to adfs)",
            "content": {
                "application/json": {
                    "examples": {
                        "example": {
                            "summary": "Multi-status (for redirect to adfs)",
                            "value": {
                                "status": "Multi-status (for redirect to adfs)",
                                "url": "url for redirect",
                            },
                        },
                    },
                },
            },
        }
    }
    template_400 = {
        400: {
            "description": "Invalid Request",
            "content": {
                "application/json": {
                    "examples": {
                        "example": {
                            "summary": "Template Value",
                            "value": {
                                "status": "Invalid Request",
                                "description": "some text",
                            },
                        },
                    },
                },
            },
        }
    }
    template_401 = {
        401: {
            "description": "Not Authenticated",
            "content": {
                "application/json": {
                    "examples": {
                        "example": {
                            "summary": "Template Value",
                            "value": {
                                "status": "Not Authenticated",
                            },
                        },
                    },
                },
            },
        }
    }
    template_403 = {
        403: {
            "description": "Api Service Unavailable",
            "content": {
                "application/json": {
                    "examples": {
                        "example": {
                            "summary": "Template Value",
                            "value": {
                                "status": "Api Service Unavailable",
                            },
                        },
                    },
                },
            },
        }
    }
    template_404 = {
        404: {
            "description": "Method Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "example": {
                            "summary": "Template Value",
                            "value": {
                                "status": "Method Not Found",
                            },
                        },
                    },
                },
            },
        }
    }
    template_500 = {
        500: {
            "description": "Internal Error",
            "content": {
                "application/json": {
                    "examples": {
                        "example": {
                            "summary": "Template Value",
                            "value": {
                                "status": "Internal Error",
                                "description": "error description",
                            },
                        }
                    },
                },
            },
        }
    }


class TemplateResponsesNamespace:
    @staticmethod
    def template_200(data: dict = None, cookies: dict = {}) -> JSONResponse:
        response = JSONResponse(
            content=data,
            status_code=200,
        )
        for key, value in cookies.items():
            response.set_cookie(key=key, value=value)
        return response

    @staticmethod
    def template_400(
        data: dict = {
            "status": "Invalid Request",
        }
    ) -> JSONResponse:
        return JSONResponse(
            content=data,
            status_code=400,
        )

    @staticmethod
    def template_401() -> JSONResponse:
        return JSONResponse(
            {
                "status": "Not Authenticated",
            },
            status_code=401,
        )

    @staticmethod
    def template_403() -> JSONResponse:
        return JSONResponse(
            {
                "status": "Api Service Unavailable",
            },
            status_code=403,
        )

    @staticmethod
    def template_404() -> JSONResponse:
        return JSONResponse(
            {
                "status": "Method Not Found",
            },
            status_code=404,
        )

    @staticmethod
    def template_500(error_text: str) -> JSONResponse:
        return JSONResponse(
            {
                "status": "Internal Error",
                "description": error_text,
            },
            status_code=500,
        )
