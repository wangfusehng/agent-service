class ApplicationException(Exception):
    """应用业务异常基类"""

    status_code:int = 500 #默认http状态码
    code:str = "APPLICATION_EXCEPTION" #默认异常错误码
    message:str ="服务器内部错误"#默认异常消息

