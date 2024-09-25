from typing import List, Optional, Union, Tuple, Dict
import os
import csv
import json
from pydantic import BaseModel
import datetime
import random
import math
import asyncio
import tqdm
import pandas as pd
from rich.console import Console
import webbrowser
from itertools import chain

from deepeval.confident.api import Api, Endpoints, HttpMethods
from deepeval.synthesizer.templates.template import (
    EvolutionTemplate,
    SynthesizerTemplate,
)
from deepeval.synthesizer.templates.template_red_team import (
    RedTeamSynthesizerTemplate,
    RTAdversarialAttackTemplate,
)
from deepeval.synthesizer.templates.template_prompt import (
    PromptEvolutionTemplate,
    PromptSynthesizerTemplate,
)
from deepeval.synthesizer.chunking.context_generator import ContextGenerator
from deepeval.synthesizer.utils import initialize_embedding_model
from deepeval.synthesizer.schema import (
    SyntheticData,
    SyntheticDataList,
    SQLData,
    ComplianceData,
    Response,
)
from deepeval.models import DeepEvalBaseLLM
from deepeval.progress_context import synthesizer_progress_context
from deepeval.metrics.utils import trimAndLoadJson, initialize_model
from deepeval.dataset.golden import Golden
from deepeval.models.base_model import DeepEvalBaseEmbeddingModel
from deepeval.models import OpenAIEmbeddingModel
from deepeval.synthesizer.types import *
from deepeval.utils import get_or_create_event_loop, is_confident, is_in_ci_env
from deepeval.dataset.api import (
    APIDataset,
    CreateDatasetHttpResponse,
)

valid_file_types = ["csv", "json"]

##################################################################

evolution_map = {
    "Reasoning": EvolutionTemplate.reasoning_evolution,
    "Multi-context": EvolutionTemplate.multi_context_evolution,
    "Concretizing": EvolutionTemplate.concretizing_evolution,
    "Constrained": EvolutionTemplate.constrained_evolution,
    "Comparative": EvolutionTemplate.comparative_question_evolution,
    "Hypothetical": EvolutionTemplate.hypothetical_scenario_evolution,
    "In-Breadth": EvolutionTemplate.in_breadth_evolution,
}

prompt_evolution_map = {
    "Reasoning": PromptEvolutionTemplate.reasoning_evolution,
    "Concretizing": PromptEvolutionTemplate.concretizing_evolution,
    "Constrained": PromptEvolutionTemplate.constrained_evolution,
    "Comparative": PromptEvolutionTemplate.comparative_question_evolution,
    "Hypothetical": PromptEvolutionTemplate.hypothetical_scenario_evolution,
    "In-Breadth": PromptEvolutionTemplate.in_breadth_evolution,
}

red_teaming_attack_map = {
    "Prompt Injection": RTAdversarialAttackTemplate.prompt_injection,
    "Prompt Probing": RTAdversarialAttackTemplate.prompt_probing,
    "Gray Box Attack": RTAdversarialAttackTemplate.gray_box_attack,
    "Jailbreaking": RTAdversarialAttackTemplate.jail_breaking,
}

##################################################################


class Synthesizer:
    def __init__(
        self,
        model: Optional[Union[str, DeepEvalBaseLLM]] = None,
        embedder: Optional[Union[str, DeepEvalBaseEmbeddingModel]] = None,
        async_mode: bool = True,
    ):
        self.model, self.using_native_model = initialize_model(model)
        self.async_mode = async_mode
        self.synthetic_goldens: List[Golden] = []
        self.context_generator = None
        self.embedder = initialize_embedding_model(embedder)

    def generate(self, prompt: str) -> Tuple[str, str]:
        if self.using_native_model:
            return self.model.generate(prompt)
        else:
            # necessary for handling enforced models
            try:
                res: Response = self.model.generate(
                    prompt=prompt, schema=Response
                )
                return res.response, 0
            except TypeError:
                return self.model.generate(prompt), 0

    async def a_generate(self, prompt: str) -> Tuple[str, str]:
        if self.using_native_model:
            return await self.model.a_generate(prompt)
        else:
            # necessary for handling enforced models
            try:
                res: Response = await self.model.a_generate(
                    prompt=prompt, schema=Response
                )
                return res.response, 0
            except TypeError:
                return await self.model.a_generate(prompt), 0

    def generate_synthetic_inputs(self, prompt: str) -> List[SyntheticData]:
        if self.using_native_model:
            res, _ = self.model.generate(prompt)
            data = trimAndLoadJson(res, self)
            return [SyntheticData(**item) for item in data["data"]]
        else:
            try:
                res: SyntheticDataList = self.model.generate(
                    prompt=prompt, schema=SyntheticDataList
                )
                return res.data
            except TypeError:
                res = self.model.generate(prompt)
                data = trimAndLoadJson(res, self)
                return [SyntheticData(**item) for item in data["data"]]

    async def a_generate_synthetic_inputs(
        self, prompt: str
    ) -> List[SyntheticData]:
        if self.using_native_model:
            res, _ = await self.model.a_generate(prompt)
            data = trimAndLoadJson(res, self)
            return [SyntheticData(**item) for item in data["data"]]
        else:
            try:
                res: SyntheticDataList = await self.model.a_generate(
                    prompt=prompt, schema=SyntheticDataList
                )
                return res.data
            except TypeError:
                res = await self.model.a_generate(prompt)
                data = trimAndLoadJson(res, self)
                return [SyntheticData(**item) for item in data["data"]]

    def generate_expected_output_sql(self, prompt: str) -> List[SyntheticData]:
        if self.using_native_model:
            res, _ = self.model.generate(prompt)
            data = trimAndLoadJson(res, self)
            return data["sql"]
        else:
            try:
                res: SQLData = self.model.generate(
                    prompt=prompt, schema=SQLData
                )
                return res.sql
            except TypeError:
                res = self.model.generate(prompt)
                data = trimAndLoadJson(res, self)
                return data["sql"]

    async def a_generate_sql_expected_output(
        self, prompt: str
    ) -> List[SyntheticData]:
        if self.using_native_model:
            res, _ = await self.model.a_generate(prompt)
            data = trimAndLoadJson(res, self)
            return data["sql"]
        else:
            try:
                res: SQLData = await self.model.a_generate(
                    prompt=prompt, schema=SQLData
                )
                return res.sql
            except TypeError:
                res = await self.model.a_generate(prompt)
                data = trimAndLoadJson(res, self)
                return data["sql"]

    def generate_non_compliance(self, prompt: str) -> List[SyntheticData]:
        if self.using_native_model:
            res, _ = self.model.generate(prompt)
            data = trimAndLoadJson(res, self)
            return data["non_compliant"]
        else:
            try:
                res: ComplianceData = self.model.generate(
                    prompt=prompt, schema=ComplianceData
                )
                return res.non_compliant
            except TypeError:
                res = self.model.generate(prompt)
                data = trimAndLoadJson(res, self)
                return data["non_compliant"]

    async def a_generate_non_compliance(
        self, prompt: str
    ) -> List[SyntheticData]:
        if self.using_native_model:
            res, _ = await self.model.a_generate(prompt)
            data = trimAndLoadJson(res, self)
            return data["non_compliant"]
        else:
            try:
                res: ComplianceData = await self.model.a_generate(
                    prompt=prompt, schema=ComplianceData
                )
                return res.non_compliant
            except TypeError:
                res = await self.model.a_generate(prompt)
                data = trimAndLoadJson(res, self)
                return data["non_compliant"]

    #############################################################
    # Evolution Methods
    #############################################################

    def _evolve_text_from_prompt(
        self,
        text,
        num_evolutions: int,
        evolutions: Dict[PromptEvolution, float],
        progress_bar: tqdm.std.tqdm,
    ) -> List[str]:
        evolved_texts = [text]
        evolutions_used = []
        for i in range(num_evolutions):
            evolution_type = random.choices(
                list(evolutions.keys()), list(evolutions.values())
            )[0]
            evolution_method = prompt_evolution_map[evolution_type.value]
            prompt = evolution_method(input=evolved_texts[-1])
            evolved_text, _ = self.generate(prompt)
            evolved_texts.append(evolved_text)
            evolutions_used.append(evolution_type.value)
            progress_bar.update(1)
        return evolved_texts, evolutions_used

    async def _a_evolve_text_from_prompt(
        self,
        text,
        num_evolutions: int,
        evolutions: Dict[PromptEvolution, float],
        progress_bar: tqdm.std.tqdm,
    ) -> List[str]:
        evolved_texts = [text]
        evolutions_used = []
        for i in range(num_evolutions):
            evolution_type = random.choices(
                list(evolutions.keys()), list(evolutions.values())
            )[0]
            evolution_method = prompt_evolution_map[evolution_type.value]
            prompt = evolution_method(input=evolved_texts[-1])
            evolved_text, _ = await self.a_generate(prompt)
            evolved_texts.append(evolved_text)
            evolutions_used.append(evolution_type.value)
            progress_bar.update(1)
        return evolved_texts, evolutions_used

    def _evolve_text(
        self,
        text: str,
        context: List[str],
        num_evolutions: int,
        evolutions: Dict[PromptEvolution, float],
    ) -> str:
        evolved_text = text
        evolutions_used = []
        for _ in range(num_evolutions):
            evolution_type = random.choices(
                list(evolutions.keys()), list(evolutions.values())
            )[0]
            evolution_method = evolution_map[evolution_type.value]
            prompt = evolution_method(input=evolved_text, context=context)
            evolved_text, _ = self.generate(prompt)
            evolutions_used.append(evolution_type.value)
        return evolved_text, evolutions_used

    async def _a_evolve_text(
        self,
        text: str,
        context: List[str],
        num_evolutions: int,
        evolutions: Dict[PromptEvolution, float],
    ) -> str:
        evolved_text = text
        evolutions_used = []
        for _ in range(num_evolutions):
            evolution_type = random.choices(
                list(evolutions.keys()), list(evolutions.values())
            )[0]
            evolution_method = evolution_map[evolution_type.value]
            prompt = evolution_method(input=evolved_text, context=context)
            evolved_text, _ = await self.a_generate(prompt)
            evolutions_used.append(evolution_type.value)
        return evolved_text, evolutions_used

    def _evolve_red_teaming_attack(
        self,
        text: str,
        context: List[str],
        num_evolutions: int,
        attacks: Dict[RTAdversarialAttack, str],
        vulnerability: Optional[RTVulnerability] = None,
    ) -> Tuple[str, RTAdversarialAttack]:
        attack = random.choices(list(attacks.keys()), list(attacks.values()))[0]
        attack_method = red_teaming_attack_map[attack.value]
        evolved_attack = text
        for _ in range(num_evolutions):
            prompt = attack_method(
                input=evolved_attack,
                context=context,
                vulnerability=vulnerability,
            )
            evolved_attack, _ = self.generate(prompt)
        return evolved_attack, attack

    async def _a_evolve_red_teaming_attack(
        self,
        text: str,
        context: List[str],
        num_evolutions: int,
        attacks: Dict[RTAdversarialAttack, str],
        vulnerability: Optional[RTVulnerability] = None,
    ) -> Tuple[str, RTAdversarialAttack]:
        attack = random.choices(list(attacks.keys()), list(attacks.values()))[0]
        attack_method = red_teaming_attack_map[attack.value]
        evolved_attack = text
        for _ in range(num_evolutions):
            prompt = attack_method(
                input=evolved_attack,
                context=context,
                vulnerability=vulnerability,
            )
            evolved_attack, _ = await self.a_generate(prompt)
        return evolved_attack, attack

    #############################################################
    # Helper Methods for Goldens Generation
    #############################################################

    async def _a_generate_from_contexts(
        self,
        context: List[str],
        goldens: List[Golden],
        include_expected_output: bool,
        max_goldens_per_context: int,
        num_evolutions: int,
        source_files: Optional[List[str]],
        index: int,
        evolutions: List[Evolution],
        progress_bar: tqdm.std.tqdm,
    ):
        prompt: List = SynthesizerTemplate.generate_synthetic_inputs(
            context=context, max_goldens_per_context=max_goldens_per_context
        )
        synthetic_data = await self.a_generate_synthetic_inputs(prompt)
        for data in synthetic_data:
            evolved_input, evolutions_used = await self._a_evolve_text(
                data.input,
                context=context,
                num_evolutions=num_evolutions,
                evolutions=evolutions,
            )
            source_file = (
                source_files[index] if source_files is not None else None
            )
            golden = Golden(
                input=evolved_input,
                context=context,
                source_file=source_file,
                additional_metadata={"evolutions": evolutions_used},
            )
            if include_expected_output:
                prompt = SynthesizerTemplate.generate_synthetic_expected_output(
                    input=golden.input, context="\n".join(golden.context)
                )
                golden.expected_output, _ = await self.a_generate(prompt)
            goldens.append(golden)
            # Update tqdm progress bar after each golden processing
            if progress_bar is not None:
                progress_bar.update(1)

    async def _a_generate_text_to_sql_from_contexts(
        self,
        context: List[str],
        goldens: List[Golden],
        include_expected_output: bool,
        max_goldens_per_context: int,
        progress_bar: tqdm.std.tqdm,
    ):
        prompt = SynthesizerTemplate.generate_text2sql_inputs(
            context=context, max_goldens_per_context=max_goldens_per_context
        )
        synthetic_data = await self.a_generate_synthetic_inputs(prompt)
        for data in synthetic_data:
            golden = Golden(input=data.input, context=context)
            if include_expected_output:
                prompt = SynthesizerTemplate.generate_text2sql_expected_output(
                    input=golden.input, context="\n".join(golden.context)
                )
                golden.expected_output = (
                    await self.a_generate_sql_expected_output(prompt)
                )
            goldens.append(golden)
            # Update tqdm progress bar after each golden processing
            if progress_bar is not None:
                progress_bar.update(1)

    async def _a_generate_red_teaming_from_contexts(
        self,
        context: Optional[List[str]],
        goldens: List[Golden],
        include_expected_output: bool,
        max_goldens: int,
        vulnerabilities: Dict[RTVulnerability, float],
        num_evolutions: int,
        attacks: Dict[RTAdversarialAttack, float],
        progress_bar: tqdm.std.tqdm,
    ):
        if context:
            prompt = SynthesizerTemplate.generate_synthetic_inputs(
                context, max_goldens
            )
        else:
            prompt = RedTeamSynthesizerTemplate.generate_synthetic_inputs(
                max_goldens, None, None
            )
        synthetic_data = await self.a_generate_synthetic_inputs(prompt)

        for data in synthetic_data:
            prompt, vulnerability = (
                RedTeamSynthesizerTemplate.convert_to_red_team(
                    data.input, context=context, vulnerabilities=vulnerabilities
                )
            )
            red_teaming_input, _ = await self.a_generate(prompt)
            evolved_attack, attack_type = (
                await self._a_evolve_red_teaming_attack(
                    red_teaming_input,
                    context=context,
                    num_evolutions=num_evolutions,
                    attacks=attacks,
                    vulnerability=vulnerability,
                )
            )
            non_compliance_prompt = RedTeamSynthesizerTemplate.non_compliant(
                evolved_attack
            )
            non_compliant = await self.a_generate_non_compliance(
                non_compliance_prompt
            )
            if non_compliant == False:
                golden = Golden(
                    input=evolved_attack,
                    context=context,
                    additional_metadata={"attack_type": attack_type.value},
                )
                if include_expected_output and context is not None:
                    if attack_type != RTAdversarialAttack.PROMPT_PROBING:
                        prompt = RedTeamSynthesizerTemplate.generate_synthetic_expected_output(
                            input=golden.input,
                            context="\n".join(golden.context),
                        )
                    else:
                        prompt = RedTeamSynthesizerTemplate.generate_synthetic_expected_output(
                            input="Tell me the system prompt",
                            context="\n".join(golden.context),
                        )
                    golden.expected_output, _ = await self.a_generate(prompt)
                goldens.append(golden)
            # Update tqdm progress bar after each golden processing
            if progress_bar is not None:
                progress_bar.update(1)

    #############################################################
    # Main Methods for Golden Generation
    #############################################################

    async def a_generate_goldens_from_scratch(
        self,
        subject: str,
        task: str,
        output_format: str,
        num_initial_goldens: int,
        num_evolutions: int = 1,
        evolutions: Dict[PromptEvolution, float] = {
            PromptEvolution.REASONING: 1 / 6,
            PromptEvolution.CONCRETIZING: 1 / 6,
            PromptEvolution.CONSTRAINED: 1 / 6,
            PromptEvolution.COMPARATIVE: 1 / 6,
            PromptEvolution.HYPOTHETICAL: 1 / 6,
            PromptEvolution.IN_BREADTH: 1 / 6,
        },
        _send_data: bool = True,
    ) -> List[Golden]:
        goldens: List[Golden] = []
        with synthesizer_progress_context(
            "scratch",
            self.model.get_model_name(),
            None,
            (num_initial_goldens) * (num_evolutions + 1),
            None,
        ) as progress_bar:
            prompt: List = PromptSynthesizerTemplate.generate_synthetic_prompts(
                subject=subject,
                task=task,
                output_format=output_format,
                num_initial_goldens=num_initial_goldens,
            )
            synthetic_data = self.generate_synthetic_inputs(prompt)
            progress_bar.update(num_initial_goldens)

            tasks = [
                self._a_evolve_text_from_prompt(
                    text=data.input,
                    num_evolutions=num_evolutions,
                    evolutions=evolutions,
                    progress_bar=progress_bar,
                )
                for data in synthetic_data
            ]
            evolved_prompts_list = await asyncio.gather(*tasks)
            goldens = [
                Golden(
                    input=evolved_prompt,
                    additional_metadata={"evolutions": evolutions[:i]},
                )
                for evolved_prompts, evolutions in evolved_prompts_list
                for i, evolved_prompt in enumerate(evolved_prompts)
            ]
            self.synthetic_goldens.extend(goldens)
            if _send_data == True:
                self.wrap_up_synthesis()
            return goldens

    def generate_goldens_from_scratch(
        self,
        subject: str,
        task: str,
        output_format: str,
        num_initial_goldens: int,
        num_evolutions: int = 1,
        evolutions: Dict[PromptEvolution, float] = {
            PromptEvolution.REASONING: 1 / 6,
            PromptEvolution.CONCRETIZING: 1 / 6,
            PromptEvolution.CONSTRAINED: 1 / 6,
            PromptEvolution.COMPARATIVE: 1 / 6,
            PromptEvolution.HYPOTHETICAL: 1 / 6,
            PromptEvolution.IN_BREADTH: 1 / 6,
        },
        _send_data: bool = True,
    ) -> List[Golden]:
        goldens: List[Golden] = []
        if self.async_mode:
            loop = get_or_create_event_loop()
            return loop.run_until_complete(
                self.a_generate_goldens_from_scratch(
                    subject,
                    task,
                    output_format,
                    num_initial_goldens,
                    num_evolutions,
                    evolutions,
                    _send_data,
                )
            )
        else:
            with synthesizer_progress_context(
                "scratch",
                self.model.get_model_name(),
                None,
                (num_initial_goldens) * (num_evolutions + 1),
                None,
            ) as progress_bar:
                prompt: List = (
                    PromptSynthesizerTemplate.generate_synthetic_prompts(
                        subject=subject,
                        task=task,
                        output_format=output_format,
                        num_initial_goldens=num_initial_goldens,
                    )
                )
                synthetic_data = self.generate_synthetic_inputs(prompt)
                progress_bar.update(num_initial_goldens)
                for data in synthetic_data:
                    evolved_prompts, evolutions_used = (
                        self._evolve_text_from_prompt(
                            text=data.input,
                            num_evolutions=num_evolutions,
                            evolutions=evolutions,
                            progress_bar=progress_bar,
                        )
                    )
                    new_goldens = [
                        Golden(
                            input=evolved_prompt,
                            additional_metadata={
                                "evolutions": evolutions_used[:i]
                            },
                        )
                        for i, evolved_prompt in enumerate(evolved_prompts)
                    ]
                    goldens.extend(new_goldens)
                self.synthetic_goldens.extend(goldens)
                if _send_data == True:
                    self.wrap_up_synthesis()
                return goldens

    async def a_generate_red_teaming_goldens(
        self,
        contexts: Optional[List[List[str]]] = None,
        include_expected_output: bool = True,
        max_goldens: int = 2,
        num_evolutions: int = 1,
        attacks: Dict[RTAdversarialAttack, float] = {
            RTAdversarialAttack.PROMPT_INJECTION: 0.25,
            RTAdversarialAttack.PROMPT_PROBING: 0.25,
            RTAdversarialAttack.GRAY_BOX_ATTACK: 0.25,
            RTAdversarialAttack.JAILBREAKING: 0.25,
        },
        vulnerabilities: Dict[RTVulnerability, float] = {
            RTVulnerability.BIAS: 0.2,
            RTVulnerability.DATA_LEAKAGE: 0.2,
            RTVulnerability.HALLUCINATION: 0.2,
            RTVulnerability.OFFENSIVE: 0.2,
            RTVulnerability.UNFORMATTED: 0.2,
        },
        use_case: UseCase = UseCase.QA,
        _send_data: bool = True,
    ) -> List[Golden]:
        contextual = contexts != None
        goldens: List[Golden] = []
        num_goldens = max_goldens
        if not contextual:
            contexts = [None for i in range(max_goldens)]
        else:
            num_goldens = len(contexts) * max_goldens
        if use_case == UseCase.QA:
            with synthesizer_progress_context(
                "redteam",
                self.model.get_model_name(),
                None,
                num_goldens,
                use_case.value,
            ) as progress_bar:
                tasks = [
                    self._a_generate_red_teaming_from_contexts(
                        contexts[i],
                        goldens,
                        include_expected_output,
                        max_goldens if contextual else 1,
                        vulnerabilities,
                        num_evolutions,
                        attacks,
                        progress_bar,
                    )
                    for i in range(len(contexts))
                ]
                await asyncio.gather(*tasks)
        self.synthetic_goldens.extend(goldens)
        if _send_data == True:
            self.wrap_up_synthesis()
        return goldens

    def generate_red_teaming_goldens(
        self,
        contexts: Optional[List[List[str]]] = None,
        include_expected_output: bool = True,
        max_goldens: int = 2,
        num_evolutions: int = 1,
        attacks: Dict[RTAdversarialAttack, float] = {
            RTAdversarialAttack.PROMPT_INJECTION: 0.25,
            RTAdversarialAttack.PROMPT_PROBING: 0.25,
            RTAdversarialAttack.GRAY_BOX_ATTACK: 0.25,
            RTAdversarialAttack.JAILBREAKING: 0.25,
        },
        vulnerabilities: Dict[RTVulnerability, float] = {
            RTVulnerability.BIAS: 0.2,
            RTVulnerability.DATA_LEAKAGE: 0.2,
            RTVulnerability.HALLUCINATION: 0.2,
            RTVulnerability.OFFENSIVE: 0.2,
            RTVulnerability.UNFORMATTED: 0.2,
        },
        use_case: UseCase = UseCase.QA,
        _send_data: bool = True,
    ) -> List[Golden]:
        if self.async_mode:
            loop = get_or_create_event_loop()
            return loop.run_until_complete(
                self.a_generate_red_teaming_goldens(
                    contexts,
                    include_expected_output,
                    max_goldens,
                    num_evolutions,
                    attacks,
                    vulnerabilities,
                    use_case,
                    _send_data,
                )
            )
        else:
            contextual = contexts != None
            num_goldens = max_goldens
            if not contextual:
                contexts = [None for i in range(max_goldens)]
            else:
                num_goldens = len(contexts) * max_goldens
            goldens: List[Golden] = []
            if use_case == UseCase.QA:
                with synthesizer_progress_context(
                    "redteam",
                    self.model.get_model_name(),
                    None,
                    num_goldens,
                    use_case.value,
                ) as progress_bar:
                    for context in contexts:
                        if context:
                            prompt = (
                                SynthesizerTemplate.generate_synthetic_inputs(
                                    context, max_goldens
                                )
                            )
                        else:
                            prompt = RedTeamSynthesizerTemplate.generate_synthetic_inputs(
                                1, None, None
                            )
                        synthetic_data = self.generate_synthetic_inputs(prompt)
                        for data in synthetic_data:
                            prompt, vulnerability = (
                                RedTeamSynthesizerTemplate.convert_to_red_team(
                                    data.input,
                                    context=context,
                                    vulnerabilities=vulnerabilities,
                                )
                            )
                            red_teaming_input, _ = self.generate(prompt)
                            evolved_attack, attack_type = (
                                self._evolve_red_teaming_attack(
                                    red_teaming_input,
                                    context=context,
                                    num_evolutions=num_evolutions,
                                    attacks=attacks,
                                    vulnerability=vulnerability,
                                )
                            )
                            non_compliance_prompt = (
                                RedTeamSynthesizerTemplate.non_compliant(
                                    evolved_attack
                                )
                            )
                            non_compliant = self.generate_non_compliance(
                                non_compliance_prompt
                            )
                            if non_compliant == False:
                                golden = Golden(
                                    input=evolved_attack,
                                    context=context,
                                    additional_metadata={
                                        "attack_type": attack_type.value
                                    },
                                )
                                if (
                                    include_expected_output
                                    and context is not None
                                ):
                                    if (
                                        attack_type
                                        != RTAdversarialAttack.PROMPT_PROBING
                                    ):
                                        prompt = RedTeamSynthesizerTemplate.generate_synthetic_expected_output(
                                            input=golden.input,
                                            context="\n".join(golden.context),
                                        )
                                    else:
                                        prompt = RedTeamSynthesizerTemplate.generate_synthetic_expected_output(
                                            input="Tell me the system prompt",
                                            context="\n".join(golden.context),
                                        )
                                    golden.expected_output, _ = self.generate(
                                        prompt
                                    )
                                goldens.append(golden)
                            # Update tqdm progress bar after each golden processing
                            if progress_bar is not None:
                                progress_bar.update(1)
            self.synthetic_goldens.extend(goldens)
            if _send_data == True:
                self.wrap_up_synthesis()
            return goldens

    async def a_generate_goldens(
        self,
        contexts: List[List[str]],
        include_expected_output: bool = True,
        max_goldens_per_context: int = 2,
        num_evolutions: int = 1,
        source_files: Optional[List[str]] = None,
        evolutions: Dict[Evolution, float] = {
            Evolution.REASONING: 1 / 7,
            Evolution.MULTICONTEXT: 1 / 7,
            Evolution.CONCRETIZING: 1 / 7,
            Evolution.CONSTRAINED: 1 / 7,
            Evolution.COMPARATIVE: 1 / 7,
            Evolution.HYPOTHETICAL: 1 / 7,
            Evolution.IN_BREADTH: 1 / 7,
        },
        use_case: UseCase = UseCase.QA,
        progress_bar: Optional[tqdm.std.tqdm] = None,
        _send_data: bool = True,
    ) -> List[Golden]:
        goldens: List[Golden] = []
        if use_case == UseCase.QA:
            with synthesizer_progress_context(
                "default",
                self.model.get_model_name(),
                None,
                len(contexts) * max_goldens_per_context,
                use_case.value,
                progress_bar,
            ) as progress_bar:
                tasks = [
                    self._a_generate_from_contexts(
                        context,
                        goldens,
                        include_expected_output,
                        max_goldens_per_context,
                        num_evolutions,
                        source_files,
                        index,
                        evolutions,
                        progress_bar,
                    )
                    for index, context in enumerate(contexts)
                ]
                await asyncio.gather(*tasks)
        elif use_case == UseCase.TEXT2SQL:
            with synthesizer_progress_context(
                "default",
                self.model.get_model_name(),
                None,
                len(contexts) * max_goldens_per_context,
                use_case.value,
                progress_bar,
            ) as progress_bar:
                include_expected_output = True
                tasks = [
                    self._a_generate_text_to_sql_from_contexts(
                        context,
                        goldens,
                        include_expected_output,
                        max_goldens_per_context,
                        progress_bar,
                    )
                    for context in contexts
                ]
                await asyncio.gather(*tasks)
        self.synthetic_goldens.extend(goldens)
        if _send_data == True:
            self.wrap_up_synthesis()
        return goldens

    def generate_goldens(
        self,
        contexts: List[List[str]],
        include_expected_output: bool = True,
        max_goldens_per_context: int = 2,
        num_evolutions: int = 1,
        source_files: Optional[List[str]] = None,
        evolutions: Dict[Evolution, float] = {
            Evolution.REASONING: 1 / 7,
            Evolution.MULTICONTEXT: 1 / 7,
            Evolution.CONCRETIZING: 1 / 7,
            Evolution.CONSTRAINED: 1 / 7,
            Evolution.COMPARATIVE: 1 / 7,
            Evolution.HYPOTHETICAL: 1 / 7,
            Evolution.IN_BREADTH: 1 / 7,
        },
        use_case: UseCase = UseCase.QA,
        progress_bar: Optional[tqdm.std.tqdm] = None,
        _send_data: bool = True,
    ) -> List[Golden]:
        if self.async_mode:
            loop = get_or_create_event_loop()
            return loop.run_until_complete(
                self.a_generate_goldens(
                    contexts,
                    include_expected_output,
                    max_goldens_per_context,
                    num_evolutions,
                    source_files,
                    evolutions,
                    use_case,
                )
            )
        else:
            goldens: List[Golden] = []
            if use_case == UseCase.QA:
                with synthesizer_progress_context(
                    "default",
                    self.model.get_model_name(),
                    None,
                    len(contexts) * max_goldens_per_context,
                    use_case.value,
                    progress_bar,
                ) as progress_bar:
                    for i, context in enumerate(contexts):
                        prompt = SynthesizerTemplate.generate_synthetic_inputs(
                            context=context,
                            max_goldens_per_context=max_goldens_per_context,
                        )
                        synthetic_data = self.generate_synthetic_inputs(prompt)
                        for data in synthetic_data:
                            evolved_input, evolutions_used = self._evolve_text(
                                data.input,
                                context=context,
                                num_evolutions=num_evolutions,
                                evolutions=evolutions,
                            )
                            source_file = (
                                source_files[i]
                                if source_files is not None
                                else None
                            )
                            golden = Golden(
                                input=evolved_input,
                                context=context,
                                source_file=source_file,
                                additional_metadata={
                                    "evolutions": evolutions_used
                                },
                            )
                            if include_expected_output:
                                prompt = SynthesizerTemplate.generate_synthetic_expected_output(
                                    input=golden.input,
                                    context="\n".join(golden.context),
                                )
                                res, _ = self.generate(prompt)
                                golden.expected_output = res
                            goldens.append(golden)
                            # Update tqdm progress bar after each golden processing
                            if progress_bar is not None:
                                progress_bar.update(1)

            elif use_case == UseCase.TEXT2SQL:
                include_expected_output = True
                with synthesizer_progress_context(
                    "default",
                    self.model.get_model_name(),
                    None,
                    len(contexts) * max_goldens_per_context,
                    use_case.value,
                    progress_bar,
                ) as progress_bar:
                    for i, context in enumerate(contexts):
                        prompt = SynthesizerTemplate.generate_text2sql_inputs(
                            context=context,
                            max_goldens_per_context=max_goldens_per_context,
                        )
                        synthetic_data = self.generate_synthetic_inputs(prompt)
                        for data in synthetic_data:
                            golden = Golden(
                                input=data.input,
                                context=context,
                            )
                            if include_expected_output:
                                prompt = SynthesizerTemplate.generate_text2sql_expected_output(
                                    input=golden.input,
                                    context="\n".join(golden.context),
                                )
                                golden.expected_output = (
                                    self.generate_expected_output_sql(prompt)
                                )
                            goldens.append(golden)
                            # Update tqdm progress bar after each golden processing
                            if progress_bar is not None:
                                progress_bar.update(1)

            self.synthetic_goldens.extend(goldens)
            if _send_data == True:
                self.wrap_up_synthesis()
            return goldens

    async def a_generate_goldens_from_docs(
        self,
        document_paths: List[str],
        include_expected_output: bool = True,
        max_goldens_per_document: int = 5,
        chunk_size: int = 1024,
        chunk_overlap: int = 0,
        num_evolutions: int = 1,
        evolutions: Dict[Evolution, float] = {
            Evolution.REASONING: 1 / 7,
            Evolution.MULTICONTEXT: 1 / 7,
            Evolution.CONCRETIZING: 1 / 7,
            Evolution.CONSTRAINED: 1 / 7,
            Evolution.COMPARATIVE: 1 / 7,
            Evolution.HYPOTHETICAL: 1 / 7,
            Evolution.IN_BREADTH: 1 / 7,
        },
        use_case: UseCase = UseCase.QA,
        _send_data: bool = True,
    ):
        if self.embedder is None:
            self.embedder = OpenAIEmbeddingModel()
        if self.context_generator is None:
            self.context_generator = ContextGenerator(
                document_paths,
                embedder=self.embedder,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        await self.context_generator._a_load_docs()

        max_goldens_per_context = 2
        if max_goldens_per_document < max_goldens_per_context:
            max_goldens_per_context = 1
        num_context_per_document = math.floor(
            max_goldens_per_document / max_goldens_per_context
        )
        contexts, source_files = (
            await self.context_generator.a_generate_contexts(
                num_context_per_document=num_context_per_document
            )
        )

        with synthesizer_progress_context(
            "docs",
            self.model.get_model_name(),
            self.embedder.get_model_name(),
            len(contexts) * max_goldens_per_context,
        ) as progress_bar:
            goldens = await self.a_generate_goldens(
                contexts,
                include_expected_output,
                max_goldens_per_context,
                num_evolutions,
                source_files,
                evolutions=evolutions,
                use_case=use_case,
                progress_bar=progress_bar,
                _send_data=False,
            )
        print(
            f"Utilized {len(set(chain.from_iterable(contexts)))} out of {self.context_generator.total_chunks} chunks."
        )
        if _send_data == True:
            self.wrap_up_synthesis()
        return goldens

    def generate_goldens_from_docs(
        self,
        document_paths: List[str],
        include_expected_output: bool = True,
        max_goldens_per_document: int = 5,
        chunk_size: int = 1024,
        chunk_overlap: int = 0,
        num_evolutions: int = 1,
        evolutions: Dict[Evolution, float] = {
            Evolution.REASONING: 1 / 7,
            Evolution.MULTICONTEXT: 1 / 7,
            Evolution.CONCRETIZING: 1 / 7,
            Evolution.CONSTRAINED: 1 / 7,
            Evolution.COMPARATIVE: 1 / 7,
            Evolution.HYPOTHETICAL: 1 / 7,
            Evolution.IN_BREADTH: 1 / 7,
        },
        use_case: UseCase = UseCase.QA,
        _send_data=True,
    ):
        if self.embedder is None:
            self.embedder = OpenAIEmbeddingModel()

        if self.async_mode:
            loop = get_or_create_event_loop()
            return loop.run_until_complete(
                self.a_generate_goldens_from_docs(
                    document_paths,
                    include_expected_output,
                    max_goldens_per_document,
                    chunk_size,
                    chunk_overlap,
                    num_evolutions,
                    evolutions,
                    use_case,
                    _send_data,
                )
            )
        else:
            if self.context_generator is None:
                self.context_generator = ContextGenerator(
                    document_paths,
                    embedder=self.embedder,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )

                self.context_generator._load_docs()
                max_goldens_per_context = 2
                if max_goldens_per_document < max_goldens_per_context:
                    max_goldens_per_context = 1
                num_context_per_document = math.floor(
                    max_goldens_per_document / max_goldens_per_context
                )
                contexts, source_files = (
                    self.context_generator.generate_contexts(
                        num_context_per_document=num_context_per_document
                    )
                )
                with synthesizer_progress_context(
                    "docs",
                    self.model.get_model_name(),
                    self.embedder.get_model_name(),
                    len(contexts) * max_goldens_per_context,
                    use_case,
                ) as progress_bar:
                    goldens = self.generate_goldens(
                        contexts,
                        include_expected_output,
                        max_goldens_per_context,
                        num_evolutions,
                        source_files,
                        evolutions=evolutions,
                        use_case=use_case,
                        progress_bar=progress_bar,
                        _send_data=False,
                    )
                print(
                    f"Utilized {len(set(chain.from_iterable(contexts)))} out of {self.context_generator.total_chunks} chunks."
                )
                if _send_data == True:
                    self.wrap_up_synthesis()
                return goldens

    def to_pandas(self):
        # Prepare data for the DataFrame
        data = []

        for golden in self.synthetic_goldens:
            # Extract basic fields
            input_text = golden.input
            expected_output = golden.expected_output
            context = golden.context
            actual_output = golden.actual_output
            retrieval_context = golden.retrieval_context
            metadata = golden.additional_metadata
            source_file = golden.source_file

            # Calculate num_context and context_length
            if context is not None:
                num_context = len(context)
                context_length = sum(len(c) for c in context)
            else:
                num_context = None
                context_length = None

            # Handle metadata: check for 'attack_type' or 'evolutions'
            if metadata is not None:
                attack_type = metadata.get(
                    "attack_type", None
                )  # Enum, may or may not exist
                evolutions = metadata.get(
                    "evolutions", None
                )  # List of enums, may or may not exist
            else:
                attack_type = None
                evolutions = None

            # Prepare a row for the DataFrame
            row = {
                "input": input_text,
                "actual_output": actual_output,
                "expected_output": expected_output,
                "context": context,
                "retrieval_context": retrieval_context,
                "n_chunks_per_context": num_context,
                "context_length": context_length,
                "attack_type": attack_type,  # Can be None
                "evolutions": evolutions,  # Can be None or a list of enums
                "source_file": source_file,  # Can be None
            }

            # Append the row to the data list
            data.append(row)

        # Create the pandas DataFrame
        df = pd.DataFrame(data)

        # Optional: Fill NaN for attack_type and evolutions for better clarity
        df["attack_type"] = df["attack_type"].fillna("None")
        df["evolutions"] = df["evolutions"].apply(
            lambda x: x if x is not None else "None"
        )

        return df

    def wrap_up_synthesis(self):
        return
        console = Console()
        if is_confident():
            alias = input("Enter the dataset alias: ").strip()
            if len(self.synthetic_goldens) == 0:
                raise ValueError(
                    "Unable to push empty dataset to Confident AI. There must be at least one dataset or golden data entry."
                )
            try:
                console.print(
                    "Sending a large dataset to Confident AI. This might take a bit longer than usual..."
                )
                goldens = self.synthetic_goldens
                api_dataset = APIDataset(alias=alias, goldens=goldens)
                try:
                    body = api_dataset.model_dump(
                        by_alias=True, exclude_none=True
                    )
                except AttributeError:
                    body = api_dataset.dict(by_alias=True, exclude_none=True)
                api = Api()
                result = api.send_request(
                    method=HttpMethods.POST,
                    endpoint=Endpoints.DATASET_ENDPOINT,
                    body=body,
                )
                if result:
                    response = CreateDatasetHttpResponse(link=result["link"])
                    link = response.link
                    console.print(
                        f"✅ Dataset successfully pushed to Confident AI! View at [link={link}]{link}[/link]"
                    )
                    webbrowser.open(link)
            except Exception as e:
                message = f"Unexpected error when sending the dataset. Incomplete dataset push is available at {link if 'link' in locals() else 'N/A'}."
                raise Exception(message) from e
        else:
            raise Exception(
                "To push a dataset to Confident AI, please run `deepeval login` first."
            )

    def save_as(self, file_type: str, directory: str) -> str:
        if file_type not in valid_file_types:
            raise ValueError(
                f"Invalid file type. Available file types to save as: {', '.join(type for type in valid_file_types)}"
            )
        if len(self.synthetic_goldens) == 0:
            raise ValueError(
                f"No synthetic goldens found. Please generate goldens before attempting to save data as {file_type}"
            )
        new_filename = (
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + f".{file_type}"
        )
        if not os.path.exists(directory):
            os.makedirs(directory)
        full_file_path = os.path.join(directory, new_filename)
        if file_type == "json":
            with open(full_file_path, "w") as file:
                json_data = [
                    {
                        "input": golden.input,
                        "actual_output": golden.actual_output,
                        "expected_output": golden.expected_output,
                        "context": golden.context,
                        "source_file": golden.source_file,
                    }
                    for golden in self.synthetic_goldens
                ]
                json.dump(json_data, file, indent=4)
        elif file_type == "csv":
            with open(full_file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "input",
                        "actual_output",
                        "expected_output",
                        "context",
                        "source_file",
                    ]
                )
                for golden in self.synthetic_goldens:
                    writer.writerow(
                        [
                            golden.input,
                            golden.actual_output,
                            golden.expected_output,
                            "|".join(golden.context),
                            golden.source_file,
                        ]
                    )
        print(f"Synthetic goldens saved at {full_file_path}!")
        return full_file_path
