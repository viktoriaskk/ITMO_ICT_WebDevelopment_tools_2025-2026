"""
Проверка JWT для защищённых маршрутов; публичные пути перечислены в PUBLIC_ENDPOINTS.

Исключения согласованы с шаблоном проекта (login, register, документация).
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import List

from utils.internal_workers.auth_worker import AuthNamespace


class PermissionMiddleware(BaseHTTPMiddleware):
    """
    Middleware для проверки прав доступа к маршрутам на основе ролей пользователя.
    Пропускает публичные эндпоинты без проверки.
    """

    API_KEY_ENDPOINTS = [
        "/v1",
    ]

    PUBLIC_ENDPOINTS: List[str] = [
        "/auth/login",
        "/auth/register",
        "/docs",
        "/openapi.json",
        "/openapi-v1",
        "/redoc",
    ]

    LEGACY_ENDPOINTS: List[str] = [
        "/analyze_audio",
        "/only-for-demo",
        "/check_result",
    ]

    ADMIN_ENDPOINTS: List[str] = [
        "/service-admin",
        "/integrations",
        "/call/process-by-period",
    ]

    INTERNAL_ENDPOINTS: List[str] = [
        "/ml-callback",  # Callback от ML сервиса (защищен проверкой IP адреса)
    ]

    async def dispatch(self, request: Request, call_next):
        if any(
            request.url.path.startswith(endpoint) for endpoint in self.PUBLIC_ENDPOINTS
        ):
            return await call_next(request)

        if any(
            request.url.path.startswith(endpoint) for endpoint in self.LEGACY_ENDPOINTS
        ):
            return await call_next(request)

        if any(
            request.url.path.startswith(endpoint)
            for endpoint in self.INTERNAL_ENDPOINTS
        ):
            return await call_next(request)
        
        if any(request.url.path.startswith(endpoint) for endpoint in self.API_KEY_ENDPOINTS):
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        authorization = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(
                status_code=401, content={"detail": "Authorization header missing"}
            )

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=401, content={"detail": "Invalid authorization scheme"}
                )
        except ValueError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization header format"},
            )

        # Для админских endpoints проверяем только аутентификацию, без проверки прав доступа
        if any(
            request.url.path.startswith(endpoint) for endpoint in self.ADMIN_ENDPOINTS
        ):
            try:
                user = await AuthNamespace.get_current_user(token=token)
                if not user:
                    return JSONResponse(
                        status_code=401, content={"detail": "Authentication failed"}
                    )
                # AuthNamespace.check_admin_access(user)
                request.state.user = user
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code, content={"detail": e.detail}
                )
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"detail": f"Internal server error: {str(e)}"},
                )
            return await call_next(request)

        try:
            user = await AuthNamespace.verify_route_access(request, token)
            request.state.user = user
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(
                status_code=500, content={"detail": f"Internal server error: {str(e)}"}
            )

        return await call_next(request)
