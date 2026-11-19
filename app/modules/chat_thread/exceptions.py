from app.core.exceptions import ApplicationException


class ChatThreadNotFound(ApplicationException):

    status_code = 400
    code:str="CHAT_THREAD_NOT_FOUND"
    message:str="当前会话不存在或用户异常"