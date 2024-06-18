import json

from prompts import API_REQUEST_PROMPT, API_RESPONSE_PROMPT  # change this to the path you placed the templates
from langchain.chains import APIChain
from typing import Any, Dict, Optional
from langchain.prompts import BasePromptTemplate
from langchain.requests import TextRequestsWrapper
# from langchain.schema import BaseLanguageModel
from langchain.chains.llm import LLMChain


class APowerfulAPIChain(APIChain):
    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        question = inputs[self.question_key]
        request_info = self.api_request_chain.predict(
            question=question, api_docs=self.api_docs
        )
        print(f'request info: {request_info}')

        api_url, request_method, body = request_info.split('|')

        request_func = getattr(self.requests_wrapper, request_method.lower())

        api_response = request_func(api_url, json.loads(body))

        # answer = self.api_answer_chain.predict(
        #     question=question,
        #     api_docs=self.api_docs,
        #     api_url=api_url,
        #     api_response=api_response,
        # )
        # return {self.output_key: answer}
        return {self.output_key: api_response}

    @classmethod
    def from_llm_and_api_docs(
        cls,
        llm,
        api_docs: str,
        headers: Optional[dict] = None,
        api_url_prompt: BasePromptTemplate = API_REQUEST_PROMPT,
        api_response_prompt: BasePromptTemplate = API_RESPONSE_PROMPT,
        **kwargs: Any,
    ) -> APIChain:
        """Load chain from just an LLM and the api docs."""
        get_request_chain = LLMChain(llm=llm, prompt=api_url_prompt)
        requests_wrapper = TextRequestsWrapper(headers=headers)
        get_answer_chain = LLMChain(llm=llm, prompt=api_response_prompt)
        return cls(
            api_request_chain=get_request_chain,
            api_answer_chain=get_answer_chain,
            requests_wrapper=requests_wrapper,
            api_docs=api_docs,
            **kwargs,
        )