import asyncio
from concurrent.futures import Future, ThreadPoolExecutor, TimeoutError, wait
from typing import Any, Generic, List, Optional, Type, TypeVar

import nest_asyncio
from pydantic import BaseModel, Field

from ..agent_class import Agent
from ..llm import LLMBase
from .base import DiscussionResult, MultiAgentBase

T = TypeVar("T")

nest_asyncio.apply()

from concurrent.futures import Future, TimeoutError


class BlockingFuture:
    def __init__(self, future: Future, event: asyncio.Event):
        self._future = future
        self._event = event

    async def _wait_for_event(self, timeout=None):
        """Asynchronous helper to wait for the event."""
        if timeout is not None:
            await asyncio.wait_for(self._event.wait(), timeout)
        else:
            await self._event.wait()

    def result(self, timeout=None):
        """Block and wait for the future to be ready."""
        # Get the current event loop
        loop = asyncio.get_event_loop()

        # Schedule the _wait_for_event coroutine and block until it completes
        loop.run_until_complete(self._wait_for_event(timeout))

        if not self._future.done():
            raise TimeoutError("Operation timed out waiting for the result.")

        return self._future.result()


class BrainIteration(BaseModel):
    self_thought: str = Field(
        ...,
        description="Oriente o LLM com instruções sobre como abordar a query para a iteração atual com base no "
                    "histórico.",
    )
    iteration_stop: bool = Field(
        ...,
        description="False para continuar, True para parar a iteração, pois o LLM deu a resposta final confiável para "
                    "a query.",
    )


class ConversationTurn(BaseModel):
    iteration: int
    brain_thought: str
    llm_response: Any
    is_final: bool


class LLMResponseIteration(BaseModel):
    response: str = Field(
        ...,
        description="Resposta à discussão do cérebro cognitivo interno para a iteração atual.",
    )


class AIOT(Generic[T]):
    def __init__(
            self,
            llm: LLMBase,
            iterations: int = 5,
            answer_schema: Optional[Type[T]] = None,
            brain_agent_name: str = "Agente de Reflexão Cognitiva",
            brain_agent_role: str = "",
            brain_agent_function: str = "",
            llm_agent_name: str = "LLM",
            llm_agent_role: str = "",
            llm_agent_function: str = "",
    ):
        self.llm = llm
        self.max_iterations = iterations
        self.answer_schema = answer_schema or str
        self._loop = asyncio.get_event_loop()
        self._executor = ThreadPoolExecutor(max_workers=1)
        self.brain_agent = Agent(
            name=brain_agent_name,
            role=brain_agent_role,
            function=brain_agent_function,
        )
        self.llm_agent = Agent(
            name=llm_agent_name,
            role=llm_agent_role,
            function=llm_agent_function,
        )

    def get_llm_schema(self):
        class LLMResponse(BaseModel):
            response: self.answer_schema = Field(
                ...,
                description="A resposta gerada pelo LLM ao prompt do cérebro.",
            )
            answer_to_query: bool = Field(
                ...,
                description="A resposta contém a resposta final para a consulta? True se sim, False se não.",
            )

        return LLMResponse

    def _create_brain_agent(self):
        return self.brain_agent

    def _create_llm_agent(self):
        return self.llm_agent

    def _create_context(self, query: str):
        return {
            "query": query,
            "prompt_history": f"**Importante** Query inicial: {query}\n\n",
            "conversation": [],
        }

    async def run_async(self, query: str) -> DiscussionResult[T]:
        context = self._create_context(query)
        return await self._run_async(context)

    def run(self, query: str) -> DiscussionResult[T]:
        """
        Blocking method to run the AIOT discussion.
        Can be called from Jupyter notebooks or any synchronous context.
        """

        def run_async_in_new_loop():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            return new_loop.run_until_complete(self.run_async(query))

        return self._executor.submit(run_async_in_new_loop).result()

    async def _run_async(self, context: dict) -> DiscussionResult[T]:
        iteration = 1
        completed = False
        answer_to_query = False

        while (
                iteration <= self.max_iterations and not completed and not answer_to_query
        ):
            brain_ans = await self._brain_iteration(context, iteration)
            if brain_ans is None:
                print("Brain iteration failed. Ending discussion.")
                break

            completed = brain_ans.iteration_stop

            llm_ans = await self._llm_iteration(context, brain_ans.self_thought)
            if llm_ans is None:
                print("LLM iteration failed. Ending discussion.")
                break

            answer_to_query = llm_ans.answer_to_query

            context["conversation"].append(
                ConversationTurn(
                    iteration=iteration,
                    brain_thought=brain_ans.self_thought,
                    llm_response=llm_ans.response,
                    is_final=completed or answer_to_query,
                )
            )

            context[
                "prompt_history"
            ] += f"{self.brain_agent.name}: {brain_ans.self_thought}\nLLM answer: {llm_ans.response}\n\n"
            iteration += 1

        return DiscussionResult(
            query=context["query"],
            thoughts=context["conversation"],
            answer=llm_ans.response if llm_ans else "Unknown",
        )

    async def _brain_iteration(
            self, context: dict, iteration: int
    ) -> Optional[BrainIteration]:
        prompt_with_history = f"""{context["prompt_history"]}\n Iteração atual : {iteration}\n
        Faça o LLM responder dentro de no máximo {self.max_iterations} iterações\n\n Idealize primeiro com o LLM e 
        oriente o LLM em direção à resposta, considerando as iterações restantes.\n\n. Fale e prompt o LLM em segunda 
        pessoa diretamente, como se estivesse discutindo com o LLM para orientá-lo em direção à resposta.\n"""
        system_prompt, user_prompt = self.brain_agent.prompt(prompt_with_history)
        formatted_prompt = self.llm.format_prompt(system_prompt, user_prompt)
        return await self.llm.generate_async(formatted_prompt, BrainIteration)

    async def _llm_iteration(self, context: dict, brain_thought: str):
        prompt_with_history = (
            f"{context['prompt_history']}\nCerébro cognitivo interno: {brain_thought}\n"
            f"Com base na discussão acima, tendo o cérebro em mente.\n"
            f"Responda ao prompt do cérebro para a pergunta, indicando se é a resposta correta final para a "
            f"pergunta/instrução.\n"
            f"Se você não tiver certeza, por favor, itere com o cérebro. Certifique-se de responder com no máximo {self.max_iterations} iterações\n\n"
            f"Query original: {context['query']}\n"
        )
        system_prompt, user_prompt = self.llm_agent.prompt(prompt_with_history)
        formatted_prompt = self.llm.format_prompt(system_prompt, user_prompt)
        return await self.llm.generate_async(formatted_prompt, self.get_llm_schema())


class GIOT(Generic[T]):
    def __init__(
            self,
            llm: LLMBase,
            iterations: int = 5,
            answer_schema: Optional[Type[T]] = None,
            brain_agent_name: str = "Agente de Reflexão Cognitiva",
            brain_agent_role: str = "",
            brain_agent_function: str = "",
            llm_agent_name: str = "LLM",
            llm_agent_role: str = "",
            llm_agent_function: str = "",
    ):
        self.llm = llm
        self.total_iterations = iterations
        self.answer_schema = answer_schema or str
        self.brain_agent = Agent(
            name=brain_agent_name,
            role=brain_agent_role,
            function=brain_agent_function,
        )
        self.llm_agent = Agent(
            name=llm_agent_name,
            role=llm_agent_role,
            function=llm_agent_function,
        )
        self._loop = asyncio.get_event_loop()
        self._executor = ThreadPoolExecutor(max_workers=1)

    def get_final_llm_schema(self):
        class LLMFinalResponse(BaseModel):
            response: self.answer_schema = Field(
                ..., description="Resposta final à query"
            )
            explanation: str = Field(
                ..., description="Explicação da resposta final à query"
            )

        return LLMFinalResponse

    def _create_brain_agent(self):
        return self.brain_agent

    def _create_llm_agent(self):
        return self.llm_agent

    def _create_context(self, query: str):
        return {
            "query": query,
            "prompt_history": f"**Importante** Query inicial: {query}\n\n",
            "conversation": [],
        }

    def run(self, query: str) -> DiscussionResult[T]:
        """
        Blocking method to run the AIOT discussion.
        Can be called from Jupyter notebooks or any synchronous context.
        """

        def run_async_in_new_loop():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            return new_loop.run_until_complete(self.run_async(query))

        return self._executor.submit(run_async_in_new_loop).result()

    async def run_async(self, query: str) -> DiscussionResult[T]:
        context = self._create_context(query)
        return await self._run_async(context)

    async def _run_async(self, context: dict) -> DiscussionResult[T]:
        llm_ans = None
        for current_iteration in range(1, self.total_iterations + 1):
            brain_ans = await self._brain_iteration(context, current_iteration)
            if brain_ans is None:
                print(f"Brain iteration {current_iteration} failed. Ending discussion.")
                break

            llm_ans = await self._llm_iteration(
                context, brain_ans.self_thought, current_iteration
            )
            if llm_ans is None:
                print(f"LLM iteration {current_iteration} failed. Ending discussion.")
                break

            context["conversation"].append(
                ConversationTurn(
                    iteration=current_iteration,
                    brain_thought=brain_ans.self_thought,
                    llm_response=llm_ans.response,
                    is_final=False,
                )
            )

            context[
                "prompt_history"
            ] += f"Iteração {current_iteration}/{self.total_iterations}:\n{self.brain_agent.name}: {brain_ans.self_thought}\n{self.llm_agent.name} answer: {llm_ans.response}\n\n"

        final_answer = await self._llm_final_iteration(context)

        return DiscussionResult(
            query=context["query"],
            thoughts=context["conversation"],
            answer=final_answer.response if final_answer else "Unknown",
        )

    async def _brain_iteration(
            self, context: dict, current_iteration: int
    ) -> Optional[BrainIteration]:
        prompt_with_history = (
            f"{context['prompt_history']}\n"
            f"Iteração atual: {current_iteration}/{self.total_iterations}\n"
            f"Oriente o LLM em direção à resposta, considerando as iterações restantes.\n\n"
            f"Converse e estimule o LLM diretamente, como se estivesse discutindo com ele, para orientá-lo em direção à resposta.\n"
            f"Query original: {context['query']}\n"
        )
        system_prompt, user_prompt = self.brain_agent.prompt(prompt_with_history)
        formatted_prompt = self.llm.format_prompt(system_prompt, user_prompt)
        return await self.llm.generate_async(formatted_prompt, BrainIteration)

    async def _llm_iteration(
            self, context: dict, brain_thought: str, current_iteration: int
    ) -> Optional[LLMResponseIteration]:
        prompt_with_history = (
            f"{context['prompt_history']}\n"
            f"Cerébro cognitivo interno: {brain_thought}\n"
            f"Iteração atual: {current_iteration}/{self.total_iterations}\n"
            f"Discuta mais com o cérebro para chegar a uma resposta. Não forneça uma resposta final ainda.\n"
            f"Query original: {context['query']}\n"
        )
        system_prompt, user_prompt = self.llm_agent.prompt(prompt_with_history)
        formatted_prompt = self.llm.format_prompt(system_prompt, user_prompt)
        return await self.llm.generate_async(formatted_prompt, LLMResponseIteration)

    async def _llm_final_iteration(self, context: dict):
        prompt_with_history = (
            f"{context['prompt_history']}\n"
            f"Você está na iteração final: com base na discussão acima entre você e o cérebro, forneça sua resposta "
            f"final para a query.\n"
            f"Query original: {context['query']}\n"
        )
        system_prompt, user_prompt = self.llm_agent.prompt(prompt_with_history)
        formatted_prompt = self.llm.format_prompt(system_prompt, user_prompt)
        return await self.llm.generate_async(
            formatted_prompt, self.get_final_llm_schema()
        )
