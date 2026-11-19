from contextlib import asynccontextmanager
from urllib.request import Request
import sys
from app.infra.checkpointer import (
    close_checkpointer,
    init_checkpointer,
)
import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.core.exceptions import ApplicationException
from app.core.logging import configure_logging,get_logger
from app.core.config import settings
from app.infra.database import check_database, close_database
from app.modules.chat_thread.exceptions import ChatThreadNotFound
from app.agents.insurance_advisor import init_insurance_agent
#日志配置
configure_logging(settings.logging.level)
#获取日志记录器
logger = get_logger(__name__)

#初始化生命周期钩子函数
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"【{settings.app.name}】应用启动中...")

    from app.infra.database import check_database, close_database

    try:
        # 1.检查业务数据库连接
        await check_database()
        # 2.初始化Checkpointer
        checkpointer = await init_checkpointer()
        # 3.初始化agent存放在FastAPI的共享状态中
        app.state.agent = init_insurance_agent(checkpointer)

        yield
    finally:
        logger.info("应用关闭中... ")
        # 3.关闭Checkpointer连接池
        await close_checkpointer()
        # 4.关闭SQLAlchemy连接池
        await close_database()

#初始化FastAPI
app = FastAPI(
    title=settings.app.name,
    debug=settings.app.debug,
    lifespan=lifespan
)
# 统一处理异常信息，发现是ChatThreadNotFound异常，返回对应的错误状态码和错误信息
@app.exception_handler(ApplicationException)
def handle_exception(request: Request, exc: ApplicationException):
    logger.error(f"处理异常, 请求路径: {request.url}, 异常信息: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
        }
    )
from app.modules.product.router import router as product_router
from app.modules.chat_thread.router import router as chat_thread_router
from app.modules.chat.router import router as chat_router

app.include_router(product_router)
app.include_router(chat_thread_router)
app.include_router(chat_router)

# 健康检查测试接口‘
@app.get("/healthy",summary="健康检查接口")
async def health_check()->dict[str,str]:
    logger.info("健康检查接口正常调用")
    return {"status":"ok"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=False,
        loop= "asyncio:SelectorEventLoop" if sys.platform == "win32" else "auto",
    )