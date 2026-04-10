"""
Декоратор для core-функций: логирование аргументов (без секретов) и перехват исключений.

Оборачивает implementation-функции, чтобы единообразно писать в лог и отдавать JSON-ошибки.
"""

import json
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from templates.responses import TemplateResponsesNamespace
from utils.internal_workers.auth_worker import AuthNamespace
from utils.logger import logger

def custom_core_decorator(func):
    async def wrapper(*args, **kwargs):
        combined_args = {}
        for key, value in kwargs.items():
            if isinstance(value, BaseModel):
                combined_args[key] = value.dict()
            elif isinstance(value, UploadFile):
                combined_args[key] = {
                    "filename": value.filename,
                    "content_type": value.content_type,
                }
            else:
                try:
                    json.dumps(value)
                    combined_args[key] = value
                except (TypeError, ValueError):
                    combined_args[key] = str(value)

        try:
            del combined_args["access_token"]
            del combined_args["refresh_token"]
        except Exception:
            pass

        try:
            token = kwargs.get("token")
            if token is not None:
                user = await AuthNamespace.get_current_user(token=token)
                user_id = user.id
            else:
                user_id = 1
        except Exception:
            user_id = 1

        try:
            result: JSONResponse = await func(*args, **kwargs)
            try:
                logger.info(
                    f"Success: {func.__name__} - User {user_id} - "
                    f"Params {combined_args} - Status {result.status}"
                )
            except:
                logger.info(
                    f"Success: {func.__name__} - User {user_id} - "
                    f"Params {combined_args}"
                )
            # await CustomLogsNamespace.out_log_entry(
            #     status_code=result.status_code,
            #     user_id=user_id,
            #     app_name=func.__name__,
            #     call_params=combined_args,
            # )
            return result
        except Exception as exception:
            result = TemplateResponsesNamespace.template_500(error_text=str(exception))

            logger.error(
                f"Error: {func.__name__} - User {user_id} - "
                f"Params {combined_args} - Error {exception}"
            )

            # await CustomLogsNamespace.error_log_entry(
            #     response_body=json.loads(result.body.decode("utf-8")),
            #     user_id=user_id,
            #     app_name=func.__name__,
            #     call_params=combined_args,
            # )
            return result

    return wrapper
