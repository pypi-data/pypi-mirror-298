import os
import json
from typing import (
    Any,
    List,
    Dict,
    Union,
    Optional,
    AsyncGenerator
)

import aiohttp
import asyncio
import requests

from qwergpt.schema import Message
from qwergpt.llm.base import LLM
from qwergpt.llm.errors import (
    LLMBalanceDepletionError,
    LLMAPIOverload,
    LLMAPIUnknownError,
)


class ZhipuMessage(Message):
    content: Union[str, List[Dict[str, Any]]]


class ZhipuLLM(LLM):
    API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
    ERROR_CODES = {
        'BALANCE_DEPLETION': '1113',
        'API_OVERLOAD': ['1305', '1302']
    }

    _semaphore = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_semaphore(cls):
        async with cls._lock:
            if cls._semaphore is None:
                cls._semaphore = asyncio.Semaphore(20)
        return cls._semaphore

    def __init__(self, model_name='glm-4-air') -> None:
        super().__init__("ZhipuLLM")
        self.api_key = os.getenv('ZHIPUAI_API_KEY')
        self.model_name = model_name

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def _prepare_request_data(self, messages: List[ZhipuMessage], max_tokens: int, stream: bool = False) -> dict:
        request_data = {
            "model": self.model_name,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "stream": stream,
        }

        if max_tokens > 0:
            request_data["max_tokens"] = max_tokens
        
        return request_data
    
    def _handle_error(self, res: dict):
        if 'error' in res:
            error_code = res['error'].get('code')
            if error_code == self.ERROR_CODES['BALANCE_DEPLETION']:
                raise LLMBalanceDepletionError("Account balance depleted. Please recharge.")
            elif error_code in self.ERROR_CODES['API_OVERLOAD']:
                raise LLMAPIOverload('LLM API Overload.')
            else:
                print(f"LLM Error: {res['error']}")
                raise LLMAPIUnknownError('LLM Unknown Error')

    def complete(self, messages: List[Message], max_tokens=1024, metadata=False) -> Message:        
        headers = self._get_headers()
        data = self._prepare_request_data(messages, max_tokens)

        response = requests.post(self.API_URL, headers=headers, json=data)
        res = response.json()

        self._handle_error(res)

        usage = res['usage']
        self.update_token_count(
            usage['prompt_tokens'],
            usage['completion_tokens'],
            usage['total_tokens']
        )

        content = res['choices'][0]['message']['content']
        return Message(role='assistant', content=content)
    
    async def acomplete(self, messages: List[ZhipuMessage], max_tokens: int = 4095, metadata=False) -> Message:
        semaphore = await self.get_semaphore()
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                headers = self._get_headers()
                data = self._prepare_request_data(messages, max_tokens)

                timeout = aiohttp.ClientTimeout()
                async with session.post(self.API_URL, headers=headers, json=data, timeout=timeout) as response:
                    res = await response.json()

                self._handle_error(res)

                usage = res['usage']
                self.update_token_count(
                    usage['prompt_tokens'],
                    usage['completion_tokens'],
                    usage['total_tokens']
                )

                content = res['choices'][0]['message']['content']
                return Message(role='assistant', content=content)

    async def acomplete_stream(self, messages: List[Message], max_tokens: int = 4095, metadata=False) -> AsyncGenerator[Message, None]:
        semaphore = await self.get_semaphore()
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                headers = self._get_headers()
                data = self._prepare_request_data(messages, max_tokens, stream=True)
                async with session.post(self.API_URL, headers=headers, json=data) as response:
                    async for line in response.content:
                        message = self._process_stream_line(line)
                        if message:
                            yield message

    def _process_stream_line(self, line: bytes) -> Optional[Message]:
        try:
            chunk = line.decode('utf-8').strip()
            if chunk.startswith('data:'):
                chunk = chunk[5:].strip()
            if chunk == '[DONE]':
                return None
            if chunk:
                chunk_data = json.loads(chunk)
                if 'choices' in chunk_data and chunk_data['choices']:
                    if chunk_data['choices'][0].get('finish_reason', '') == 'stop':
                        usage = chunk_data['usage']
                        self.update_token_count(
                            usage['prompt_tokens'],
                            usage['completion_tokens'],
                            usage['total_tokens']
                        )
                    
                    delta = chunk_data['choices'][0].get('delta', {})
                    content = delta.get('content', '')
                    if content:
                        return Message(role='assistant', content=content)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON: {chunk}")
        except Exception as e:
            print(f"Error processing stream: {str(e)}")
        return None
