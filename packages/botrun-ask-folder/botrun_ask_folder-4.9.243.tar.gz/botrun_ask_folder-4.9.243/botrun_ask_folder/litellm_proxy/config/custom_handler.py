import litellm
from litellm.types.utils import GenericStreamingChunk, ModelResponse
from typing import Iterator, AsyncIterator
from litellm import CustomLLM, Choices
import uuid
import os
import asyncio

from botrun_ask_folder.query_qdrant import query_qdrant_and_llm
from dotenv import load_dotenv

from botrun_ask_folder.botrun_reader import (
    read_notice_prompt_and_collection_from_botrun,
)


class BotrunLLMError(Exception):  # use this for all your exceptions
    def __init__(
        self,
        status_code,
        message,
    ):
        self.status_code = status_code
        self.message = message
        super().__init__(
            self.message
        )  # Call the base class constructor with the parameters it needs


class BotrunLLMParams:
    def __init__(
        self,
        qdrant_host,
        qdrant_port,
        qdrant_api_key,
        collection_name,
        chat_history,
        user_input,
        embedding_model,
        top_k,
        notice_prompt,
        chat_model,
        hnsw_ef,
        file_path_field,
        text_content_field,
        google_file_id_field,
        page_number_field,
        gen_page_imgs_field,
        ori_file_name_field,
        sheet_name_field,
        file_upload_date_field,
    ):
        self.qdrant_host = qdrant_host
        self.qdrant_port = qdrant_port
        self.qdrant_api_key = qdrant_api_key
        self.collection_name = collection_name
        self.chat_history = chat_history
        self.user_input = user_input
        self.embedding_model = embedding_model
        self.top_k = top_k
        self.notice_prompt = notice_prompt
        self.chat_model = chat_model
        self.hnsw_ef = hnsw_ef
        self.file_path_field = file_path_field
        self.text_content_field = text_content_field
        self.google_file_id_field = google_file_id_field
        self.page_number_field = page_number_field
        self.gen_page_imgs_field = gen_page_imgs_field
        self.ori_file_name_field = ori_file_name_field
        self.sheet_name_field = sheet_name_field
        self.file_upload_date_field = file_upload_date_field


class BotrunLLM(CustomLLM):
    def _get_botrun_llm_params(self, *args, **kwargs) -> BotrunLLMParams:
        load_dotenv()
        model = kwargs.get("model", "")
        messages = kwargs.get("messages", [])
        botrun_name = model.split("-")[-1]
        folder_id = os.environ.get("GOOGLE_DRIVE_BOTS_FOLDER_ID")
        if not folder_id:
            raise BotrunLLMError(
                status_code=500,
                message="GOOGLE_DRIVE_BOTS_FOLDER_ID environment variable is not set",
            )

        # 從 botrun 檔案讀取 notice_prompt
        # chat_model = "openai/gpt-4o-2024-08-06"
        try:
            notice_prompt, collection_name, chat_model = (
                read_notice_prompt_and_collection_from_botrun(botrun_name, folder_id)
            )
            # print(f"notice_prompt: {notice_prompt}")
            # print(f"collection_name: {collection_name}")
            # print(f"_get_botrun_llm_params chat_model: {chat_model}")
        except Exception as e:
            # print(f"_get_botrun_llm_params exception: {e}")
            raise BotrunLLMError(status_code=404, message=str(e))

        # 固定字段名稱
        file_path_field = "file_path"
        text_content_field = "text_content"
        google_file_id_field = "google_file_id"
        page_number_field = "page_number"
        gen_page_imgs_field = "gen_page_imgs"
        ori_file_name_field = "ori_file_name"
        sheet_name_field = "sheet_name"
        file_upload_date_field = "file-upload-date"
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = os.getenv("QDRANT_PORT", 6333)
        qdrant_api_key = os.getenv("QDRANT_API_KEY", "")
        embedding_model = "openai/text-embedding-3-large"
        top_k = 6
        hnsw_ef = 256

        chat_history = messages[:-1] if len(messages) > 1 else []
        user_input = messages[-1]["content"] if messages else ""
        return BotrunLLMParams(
            qdrant_host,
            qdrant_port,
            qdrant_api_key,
            collection_name,
            chat_history,
            user_input,
            embedding_model,
            top_k,
            notice_prompt,
            chat_model,
            hnsw_ef,
            file_path_field,
            text_content_field,
            google_file_id_field,
            page_number_field,
            gen_page_imgs_field,
            ori_file_name_field,
            sheet_name_field,
            file_upload_date_field,
        )

    def completion(self, *args, **kwargs) -> litellm.ModelResponse:
        print("BotrunLLM.completion")
        # 使用事件循環運行異步的 acompletion 方法
        return asyncio.run(self.acompletion(*args, **kwargs))

    async def acompletion(self, *args, **kwargs) -> litellm.ModelResponse:
        print("BotrunLLM.acompletion")
        # print("Args:", json.dumps(args, indent=2, default=str))
        # print("Kwargs:", json.dumps(kwargs, indent=2, default=str))
        stream = kwargs.get("stream", False)
        model = kwargs.get("model", "")

        result = await self._generate_complete(
            self._get_botrun_llm_params(*args, **kwargs)
        )
        return ModelResponse(
            id=f"botrun-{uuid.uuid4()}",
            choices=[
                {
                    "message": {"role": "assistant", "content": result},
                    "finish_reason": "stop",
                }
            ],
            model=model,
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        )

    async def _sync_to_async_generator(self, sync_gen):
        for item in sync_gen:
            yield item
            await asyncio.sleep(0)  # 讓出控制權，允許其他協程運行

    async def _generate_stream(
        self, botrun_llm_params: BotrunLLMParams, model: str
    ) -> AsyncIterator[ModelResponse]:
        # print("BotrunLLM._generate_stream model:", model)
        async for fragment in self._sync_to_async_generator(
            query_qdrant_and_llm(
                botrun_llm_params.qdrant_host,
                botrun_llm_params.qdrant_port,
                botrun_llm_params.collection_name,
                botrun_llm_params.user_input,
                botrun_llm_params.embedding_model,
                botrun_llm_params.top_k,
                botrun_llm_params.notice_prompt,
                botrun_llm_params.chat_model,
                botrun_llm_params.hnsw_ef,
                botrun_llm_params.file_path_field,
                botrun_llm_params.text_content_field,
                botrun_llm_params.google_file_id_field,
                botrun_llm_params.page_number_field,
                botrun_llm_params.gen_page_imgs_field,
                botrun_llm_params.ori_file_name_field,
                botrun_llm_params.sheet_name_field,
                botrun_llm_params.file_upload_date_field,
                include_ref_page=False,
                chat_history=botrun_llm_params.chat_history,
                qdrant_api_key=botrun_llm_params.qdrant_api_key,
            )
        ):
            # print("BotrunLLM._generate_stream fragment:", fragment)
            yield ModelResponse(
                id=f"botrun-chunk-{uuid.uuid4()}",
                choices=[{"delta": {"content": fragment}, "finish_reason": None}],
                model=f"botrun/{model}",
                stream=True,
            )
        # print("BotrunLLM._generate_stream finish")
        yield ModelResponse(
            id=f"botrun-chunk-{uuid.uuid4()}",
            choices=[{"delta": {"content": ""}, "finish_reason": "stop"}],
            model=f"botrun/{model}",
            stream=True,
        )

    async def _generate_generic_stream_chunk(
        self, botrun_llm_params: BotrunLLMParams, model: str
    ) -> AsyncIterator[GenericStreamingChunk]:
        # print("BotrunLLM._generate_generic_stream_chunk model:", model)
        index = 0
        messages = botrun_llm_params.chat_history + [
            {"role": "user", "content": botrun_llm_params.user_input},
            {"role": "system", "content": botrun_llm_params.notice_prompt},
        ]
        if botrun_llm_params.collection_name is None:
            # 使用一般的 litellm streaming
            response = await litellm.acompletion(
                model=botrun_llm_params.chat_model,
                messages=messages,
                stream=True,
            )

            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield GenericStreamingChunk(
                        finish_reason=None,
                        index=index,
                        is_finished=False,
                        text=content,
                        tool_use=None,
                        usage={
                            "completion_tokens": 0,
                            "prompt_tokens": 0,
                            "total_tokens": 0,
                        },
                    )
                    index += 1

            # 最後一個 chunk
            yield GenericStreamingChunk(
                finish_reason="stop",
                index=index,
                is_finished=True,
                text="",
                tool_use=None,
                usage={
                    "completion_tokens": 0,
                    "prompt_tokens": 0,
                    "total_tokens": 0,
                },  # 您可能需要累積實際的使用量
            )
        else:
            async for fragment in self._sync_to_async_generator(
                query_qdrant_and_llm(
                    botrun_llm_params.qdrant_host,
                    botrun_llm_params.qdrant_port,
                    botrun_llm_params.collection_name,
                    botrun_llm_params.user_input,
                    botrun_llm_params.embedding_model,
                    botrun_llm_params.top_k,
                    botrun_llm_params.notice_prompt,
                    botrun_llm_params.chat_model,
                    botrun_llm_params.hnsw_ef,
                    botrun_llm_params.file_path_field,
                    botrun_llm_params.text_content_field,
                    botrun_llm_params.google_file_id_field,
                    botrun_llm_params.page_number_field,
                    botrun_llm_params.gen_page_imgs_field,
                    botrun_llm_params.ori_file_name_field,
                    botrun_llm_params.sheet_name_field,
                    botrun_llm_params.file_upload_date_field,
                    include_ref_page=False,
                    chat_history=botrun_llm_params.chat_history,
                    qdrant_api_key=botrun_llm_params.qdrant_api_key,
                )
            ):
                # print("BotrunLLM._generate_stream fragment:", fragment)
                yield GenericStreamingChunk(
                    finish_reason=None,
                    index=index,
                    is_finished=False,
                    text=fragment,
                    tool_use=None,
                    usage={
                        "completion_tokens": 10,
                        "prompt_tokens": 20,
                        "total_tokens": 30,
                    },
                )
                index += 1
            # print("BotrunLLM._generate_stream finish")
            yield GenericStreamingChunk(
                finish_reason="stop",
                index=index,
                is_finished=True,
                text="",
                tool_use=None,
                usage={
                    "completion_tokens": 10,
                    "prompt_tokens": 20,
                    "total_tokens": 30,
                },
            )

    async def _generate_complete(self, *args) -> str:
        result = ""
        botrun_llm_params = args[0]
        if botrun_llm_params.collection_name is None:
            # 使用一般的 litellm completion
            messages = botrun_llm_params.chat_history + [
                {"role": "user", "content": botrun_llm_params.user_input},
                {"role": "system", "content": botrun_llm_params.notice_prompt},
            ]
            response = await litellm.acompletion(
                model=botrun_llm_params.chat_model,
                messages=messages,
            )
            return response.choices[0].message.content
        else:
            async for fragment in self._sync_to_async_generator(
                query_qdrant_and_llm(
                    botrun_llm_params.qdrant_host,
                    botrun_llm_params.qdrant_port,
                    botrun_llm_params.collection_name,
                    botrun_llm_params.user_input,
                    botrun_llm_params.embedding_model,
                    botrun_llm_params.top_k,
                    botrun_llm_params.notice_prompt,
                    botrun_llm_params.chat_model,
                    botrun_llm_params.hnsw_ef,
                    botrun_llm_params.file_path_field,
                    botrun_llm_params.text_content_field,
                    botrun_llm_params.google_file_id_field,
                    botrun_llm_params.page_number_field,
                    botrun_llm_params.gen_page_imgs_field,
                    botrun_llm_params.ori_file_name_field,
                    botrun_llm_params.sheet_name_field,
                    botrun_llm_params.file_upload_date_field,
                    include_ref_page=False,
                    chat_history=botrun_llm_params.chat_history,
                    qdrant_api_key=botrun_llm_params.qdrant_api_key,
                )
            ):
                result += fragment
        return result

    def streaming(self, *args, **kwargs) -> Iterator[GenericStreamingChunk]:
        print("BotrunLLM.streaming")
        return self._sync_generator(self.astreaming(*args, **kwargs))

    async def astreaming(self, *args, **kwargs) -> AsyncIterator[GenericStreamingChunk]:
        model = kwargs.get("model", "")
        print("BotrunLLM.astreaming model:", model)
        async for chunk in self._generate_generic_stream_chunk(
            self._get_botrun_llm_params(*args, **kwargs), model
        ):
            yield chunk

    def _sync_generator(self, async_gen):
        while True:
            try:
                yield asyncio.run(async_gen.__anext__())
            except StopAsyncIteration:
                break


botrun_llm = BotrunLLM()
