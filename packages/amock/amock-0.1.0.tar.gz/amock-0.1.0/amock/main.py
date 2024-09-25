from typing import Dict, Any, Self, List

import json
import logging

from openai import OpenAI
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from openai.types.chat_model import ChatModel

from . import prompt


log = logging.getLogger(__name__)


def Field(
    default: Any = PydanticUndefined,
    *,
    description: str | None = None,
):
    return FieldInfo.from_field(
        default,
        description=description,
    )


class MockModel(BaseModel):
    """
    from mock import MockModel, Field

    class User(MockModel):
        name: str = Field(description="用户名")
        age: int = Field(description="年龄")
        email: str = Field(description="邮箱")
        phone: str = Field(description="电话")

    api_key = "xxx"
    base_url = "xxx"
    MockModel.init(api_key, base_url, model="gpt-3.5-turbo")
    print(User.create())
    """

    class engine:
        client: OpenAI
        model: ChatModel | str

    @classmethod
    def init(cls, api_key: str, base_url: str, model: ChatModel | str):
        cls.engine.model = model
        cls.engine.client = OpenAI(api_key=api_key, base_url=base_url)

    @classmethod
    def output_format(cls) -> Dict[str, str]:
        format = {}
        fields = cls.model_fields
        for name, field in cls.__annotations__.items():
            if issubclass(field, MockModel):
                format[name] = field.output_format()
            else:
                format[name] = f"type: {field.__qualname__}"
                if name in fields:
                    format[name] += f", description: {fields[name].description}"
        return format

    @classmethod
    def create(cls) -> Self:
        output_format = json.dumps(cls.output_format(), indent=4, ensure_ascii=False)
        content = prompt.TEST_ENGINEER.render(output_format=output_format)
        log.debug(content)
        chat_completion = cls.engine.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": content,
            }],
            model=cls.engine.model,
            response_format={"type": "json_object"},
        )
        log.debug(chat_completion.choices[0].message.content)
        return cls.model_validate_json(chat_completion.choices[0].message.content)

    @classmethod
    def batch_create(cls, output_count: int, ignore_error: bool = True) -> List[Self]:
        output_format = {
            "data": [cls.output_format()],
        }
        output_format = json.dumps(output_format, indent=4, ensure_ascii=False)
        content = prompt.TEST_ENGINEER.render(output_count=output_count, output_format=output_format)
        log.debug(content + "\n\n")
        chat_completion = cls.engine.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": content,
            }],
            model=cls.engine.model,
            response_format={"type": "json_object"},
        )
        log.debug(chat_completion.choices[0].message.content + "\n\n")
        output = json.loads(chat_completion.choices[0].message.content)
        data = []
        for item in output.get("data", []):
            try:
                data.append(cls.model_validate(item))
            except Exception as e:
                if not ignore_error:
                    raise e
        return data
