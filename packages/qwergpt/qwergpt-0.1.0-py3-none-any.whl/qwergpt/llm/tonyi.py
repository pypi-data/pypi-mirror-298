import os
import json
from typing import (
    List, 
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


class TongyiLLM(LLM):
    API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'

    _semaphore = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_semaphore(cls):
        async with cls._lock:
            if cls._semaphore is None:
                cls._semaphore = asyncio.Semaphore(20)
        return cls._semaphore

    def __init__(self, model_name='qwen-turbo') -> None:
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        self.model_name = model_name

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def _prepare_request_data(self, messages: List[Message], max_tokens: int, stream: bool = False) -> dict:
        return {
            "model": self.model_name,
            "messages": [msg.model_dump() for msg in messages],
            "stream": stream,
            "max_tokens": max_tokens,
        }

    def complete(self, messages: List[Message], max_tokens=1024, metadata=False) -> Message:        
        headers = self._get_headers()
        data = self._prepare_request_data(messages, max_tokens)

        response = requests.post(self.API_URL, headers=headers, json=data)
        res = response.json()

        content = res['choices'][0]['message']['content']
        return Message(role='assistant', content=content)
    
    async def acomplete(self, messages: List[Message], max_tokens: int = 4095, metadata=False) -> Message:
        semaphore = await self.get_semaphore()
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                headers = self._get_headers()
                data = self._prepare_request_data(messages, max_tokens)

                timeout = aiohttp.ClientTimeout()
                async with session.post(self.API_URL, headers=headers, json=data, timeout=timeout) as response:
                    res = await response.json()

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
                        if usage:
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
