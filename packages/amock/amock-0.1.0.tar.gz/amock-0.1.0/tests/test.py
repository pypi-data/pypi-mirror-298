import os
import logging

from amock import MockModel, Field


# 创建打印日志，日志等级debug
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def test_create():

    class User(MockModel):
        name: str = Field(description="用户名")
        age: int = Field(description="年龄")
        email: str = Field(description="邮箱")

    api_key = os.environ['api_key']
    base_url = os.environ.get('base_url')
    model = 'gpt-3.5-turbo'
    MockModel.init(api_key, base_url, model)
    user = User.create()
    log.info(user)


def test_batch_create():

    class User(MockModel):
        name: str = Field(description="用户名")
        age: int = Field(description="年龄")
        email: str = Field(description="邮箱")
        phone: str = Field(description="电话")

    api_key = os.environ['api_key']
    base_url = os.environ.get('base_url')
    model = 'gpt-3.5-turbo'
    model = 'gpt-3.5-turbo'
    MockModel.init(api_key, base_url, model)
    users = User.batch_create(output_count=3, ignore_error=False)
    log.info(users)


if __name__ == "__main__":
    test_create()
    test_batch_create()
