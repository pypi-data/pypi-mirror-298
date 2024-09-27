from __future__ import annotations
from typing import Dict, Any, Optional, Set
from collections import UserList
import enum

from jinja2 import Environment, meta

from edsl.prompts.Prompt import Prompt
from edsl.data_transfer_models import ImageInfo
from edsl.prompts.registry import get_classes as prompt_lookup
from edsl.exceptions import QuestionScenarioRenderError


class PromptComponent(enum.Enum):
    AGENT_INSTRUCTIONS = "agent_instructions"
    AGENT_PERSONA = "agent_persona"
    QUESTION_INSTRUCTIONS = "question_instructions"
    PRIOR_QUESTION_MEMORY = "prior_question_memory"


def get_jinja2_variables(template_str: str) -> Set[str]:
    """
    Extracts all variable names from a Jinja2 template using Jinja2's built-in parsing.

    Args:
    template_str (str): The Jinja2 template string

    Returns:
    Set[str]: A set of variable names found in the template
    """
    env = Environment()
    ast = env.parse(template_str)
    return meta.find_undeclared_variables(ast)


class PromptList(UserList):
    separator = Prompt(" ")

    def reduce(self):
        """Reduce the list of prompts to a single prompt.

        >>> p = PromptList([Prompt("You are a happy-go lucky agent."), Prompt("You are an agent with the following persona: {'age': 22, 'hair': 'brown', 'height': 5.5}")])
        >>> p.reduce()
        Prompt(text=\"""You are a happy-go lucky agent. You are an agent with the following persona: {'age': 22, 'hair': 'brown', 'height': 5.5}\""")

        """
        p = self[0]
        for prompt in self[1:]:
            if len(prompt) > 0:
                p = p + self.separator + prompt
        return p


class PromptPlan:
    """A plan for constructing prompts for the LLM call.
    Every prompt plan has a user prompt order and a system prompt order.
    It must contain each of the values in the PromptComponent enum.


    >>> p = PromptPlan(user_prompt_order=(PromptComponent.AGENT_INSTRUCTIONS, PromptComponent.AGENT_PERSONA),system_prompt_order=(PromptComponent.QUESTION_INSTRUCTIONS, PromptComponent.PRIOR_QUESTION_MEMORY))
    >>> p._is_valid_plan()
    True

    >>> p.arrange_components(agent_instructions=1, agent_persona=2, question_instructions=3, prior_question_memory=4)
    {'user_prompt': ..., 'system_prompt': ...}

    >>> p = PromptPlan(user_prompt_order=("agent_instructions", ), system_prompt_order=("question_instructions", "prior_question_memory"))
    Traceback (most recent call last):
    ...
    ValueError: Invalid plan: must contain each value of PromptComponent exactly once.

    """

    def __init__(
        self,
        user_prompt_order: Optional[tuple] = None,
        system_prompt_order: Optional[tuple] = None,
    ):
        """Initialize the PromptPlan."""

        if user_prompt_order is None:
            user_prompt_order = (
                PromptComponent.QUESTION_INSTRUCTIONS,
                PromptComponent.PRIOR_QUESTION_MEMORY,
            )
        if system_prompt_order is None:
            system_prompt_order = (
                PromptComponent.AGENT_INSTRUCTIONS,
                PromptComponent.AGENT_PERSONA,
            )

        # very commmon way to screw this up given how python treats single strings as iterables
        if isinstance(user_prompt_order, str):
            user_prompt_order = (user_prompt_order,)

        if isinstance(system_prompt_order, str):
            system_prompt_order = (system_prompt_order,)

        if not isinstance(user_prompt_order, tuple):
            raise TypeError(
                f"Expected a tuple, but got {type(user_prompt_order).__name__}"
            )

        if not isinstance(system_prompt_order, tuple):
            raise TypeError(
                f"Expected a tuple, but got {type(system_prompt_order).__name__}"
            )

        self.user_prompt_order = self._convert_to_enum(user_prompt_order)
        self.system_prompt_order = self._convert_to_enum(system_prompt_order)
        if not self._is_valid_plan():
            raise ValueError(
                "Invalid plan: must contain each value of PromptComponent exactly once."
            )

    def _convert_to_enum(self, prompt_order: tuple):
        """Convert string names to PromptComponent enum values."""
        return tuple(
            PromptComponent(component) if isinstance(component, str) else component
            for component in prompt_order
        )

    def _is_valid_plan(self):
        """Check if the plan is valid."""
        combined = self.user_prompt_order + self.system_prompt_order
        return set(combined) == set(PromptComponent)

    def arrange_components(self, **kwargs) -> Dict[PromptComponent, Prompt]:
        """Arrange the components in the order specified by the plan."""
        # check is valid components passed
        component_strings = set([pc.value for pc in PromptComponent])
        if not set(kwargs.keys()) == component_strings:
            raise ValueError(
                f"Invalid components passed: {set(kwargs.keys())} but expected {PromptComponent}"
            )

        user_prompt = PromptList(
            [kwargs[component.value] for component in self.user_prompt_order]
        )
        system_prompt = PromptList(
            [kwargs[component.value] for component in self.system_prompt_order]
        )
        return {"user_prompt": user_prompt, "system_prompt": system_prompt}

    def get_prompts(self, **kwargs) -> Dict[str, Prompt]:
        """Get both prompts for the LLM call."""
        prompts = self.arrange_components(**kwargs)
        return {
            "user_prompt": prompts["user_prompt"].reduce(),
            "system_prompt": prompts["system_prompt"].reduce(),
        }


class PromptConstructor:
    """Mixin for constructing prompts for the LLM call.

    The pieces of a prompt are:
    - The agent instructions - "You are answering questions as if you were a human. Do not break character."
    - The persona prompt - "You are an agent with the following persona: {'age': 22, 'hair': 'brown', 'height': 5.5}"
    - The question instructions - "You are being asked the following question: Do you like school? The options are 0: yes 1: no Return a valid JSON formatted like this, selecting only the number of the option: {"answer": <put answer code here>, "comment": "<put explanation here>"} Only 1 option may be selected."
    - The memory prompt - "Before the question you are now answering, you already answered the following question(s): Question: Do you like school? Answer: Prior answer"

    This is mixed into the Invigilator class.
    """

    def __init__(self, invigilator):
        self.invigilator = invigilator
        self.agent = invigilator.agent
        self.question = invigilator.question
        self.scenario = invigilator.scenario
        self.survey = invigilator.survey
        self.model = invigilator.model
        self.current_answers = invigilator.current_answers
        self.memory_plan = invigilator.memory_plan
        self.prompt_plan = PromptPlan()  # Assuming PromptPlan is defined elsewhere

        # prompt_plan = PromptPlan()

    @property
    def scenario_image_keys(self):
        image_entries = []

        for key, value in self.scenario.items():
            if isinstance(value, ImageInfo):
                image_entries.append(key)
        return image_entries

    @property
    def agent_instructions_prompt(self) -> Prompt:
        """
        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> i = InvigilatorBase.example()
        >>> i.prompt_constructor.agent_instructions_prompt
        Prompt(text=\"""You are answering questions as if you were a human. Do not break character.\""")
        """
        from edsl import Agent

        if self.agent == Agent():  # if agent is empty, then return an empty prompt
            return Prompt(text="")
        if not hasattr(self, "_agent_instructions_prompt"):
            applicable_prompts = prompt_lookup(
                component_type="agent_instructions",
                model=self.model.model,
            )
            if len(applicable_prompts) == 0:
                raise Exception("No applicable prompts found")
            self._agent_instructions_prompt = applicable_prompts[0](
                text=self.agent.instruction
            )
        return self._agent_instructions_prompt

    @property
    def agent_persona_prompt(self) -> Prompt:
        """
        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> i = InvigilatorBase.example()
        >>> i.prompt_constructor.agent_persona_prompt
        Prompt(text=\"""You are an agent with the following persona:
        {'age': 22, 'hair': 'brown', 'height': 5.5}\""")

        """
        if not hasattr(self, "_agent_persona_prompt"):
            from edsl import Agent

            if self.agent == Agent():  # if agent is empty, then return an empty prompt
                return Prompt(text="")

            if not hasattr(self.agent, "agent_persona"):
                applicable_prompts = prompt_lookup(
                    component_type="agent_persona",
                    model=self.model.model,
                )
                persona_prompt_template = applicable_prompts[0]()
            else:
                persona_prompt_template = self.agent.agent_persona

            # TODO: This multiple passing of agent traits - not sure if it is necessary. Not harmful.
            if undefined := persona_prompt_template.undefined_template_variables(
                self.agent.traits
                | {"traits": self.agent.traits}
                | {"codebook": self.agent.codebook}
                | {"traits": self.agent.traits}
            ):
                raise QuestionScenarioRenderError(
                    f"Agent persona still has variables that were not rendered: {undefined}"
                )

            persona_prompt = persona_prompt_template.render(
                self.agent.traits | {"traits": self.agent.traits},
                codebook=self.agent.codebook,
                traits=self.agent.traits,
            )
            if persona_prompt.has_variables:
                raise QuestionScenarioRenderError(
                    "Agent persona still has variables that were not rendered."
                )
            self._agent_persona_prompt = persona_prompt

        return self._agent_persona_prompt

    def prior_answers_dict(self) -> dict:
        d = self.survey.question_names_to_questions()
        for question, answer in self.current_answers.items():
            if question in d:
                d[question].answer = answer
            else:
                # adds a comment to the question
                if (new_question := question.split("_comment")[0]) in d:
                    d[new_question].comment = answer
        return d

    @property
    def question_image_keys(self):
        raw_question_text = self.question.question_text
        variables = get_jinja2_variables(raw_question_text)
        question_image_keys = []
        for var in variables:
            if var in self.scenario_image_keys:
                question_image_keys.append(var)
        return question_image_keys

    @property
    def question_instructions_prompt(self) -> Prompt:
        """
        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> i = InvigilatorBase.example()
        >>> i.prompt_constructor.question_instructions_prompt
        Prompt(text=\"""...
        ...
        """
        if not hasattr(self, "_question_instructions_prompt"):
            question_prompt = self.question.get_instructions(model=self.model.model)

            # Are any of the scenario values ImageInfo

            question_data = self.question.data.copy()

            # check to see if the question_options is actually a string
            # This is used when the user is using the question_options as a variable from a sceario
            # if "question_options" in question_data:
            if isinstance(self.question.data.get("question_options", None), str):
                env = Environment()
                parsed_content = env.parse(self.question.data["question_options"])
                question_option_key = list(
                    meta.find_undeclared_variables(parsed_content)
                )[0]

                if isinstance(
                    question_options := self.scenario.get(question_option_key), list
                ):
                    question_data["question_options"] = question_options
                    self.question.question_options = question_options

            replacement_dict = (
                {key: "<see image>" for key in self.scenario_image_keys}
                | question_data
                | {
                    k: v
                    for k, v in self.scenario.items()
                    if k not in self.scenario_image_keys
                }  # don't include images in the replacement dict
                | self.prior_answers_dict()
                | {"agent": self.agent}
                | {
                    "use_code": getattr(self.question, "_use_code", True),
                    "include_comment": getattr(
                        self.question, "_include_comment", False
                    ),
                }
            )

            rendered_instructions = question_prompt.render(replacement_dict)

            # is there anything left to render?
            undefined_template_variables = (
                rendered_instructions.undefined_template_variables({})
            )

            # Check if it's the name of a question in the survey
            for question_name in self.survey.question_names:
                if question_name in undefined_template_variables:
                    print(
                        "Question name found in undefined_template_variables: ",
                        question_name,
                    )

            if undefined_template_variables:
                raise QuestionScenarioRenderError(
                    f"Question instructions still has variables: {undefined_template_variables}."
                )

            ####################################
            # Check if question has instructions - these are instructions in a Survey that can apply to multiple follow-on questions
            ####################################
            relevant_instructions = self.survey.relevant_instructions(
                self.question.question_name
            )

            if relevant_instructions != []:
                preamble_text = Prompt(
                    text="Before answer this question, you were given the following instructions: "
                )
                for instruction in relevant_instructions:
                    preamble_text += instruction.text
                rendered_instructions = preamble_text + rendered_instructions

            self._question_instructions_prompt = rendered_instructions
        return self._question_instructions_prompt

    @property
    def prior_question_memory_prompt(self) -> Prompt:
        if not hasattr(self, "_prior_question_memory_prompt"):
            from edsl.prompts.Prompt import Prompt

            memory_prompt = Prompt(text="")
            if self.memory_plan is not None:
                memory_prompt += self.create_memory_prompt(
                    self.question.question_name
                ).render(self.scenario | self.prior_answers_dict())
            self._prior_question_memory_prompt = memory_prompt
        return self._prior_question_memory_prompt

    def create_memory_prompt(self, question_name: str) -> Prompt:
        """Create a memory for the agent.

        The returns a memory prompt for the agent.

        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> i = InvigilatorBase.example()
        >>> i.current_answers = {"q0": "Prior answer"}
        >>> i.memory_plan.add_single_memory("q1", "q0")
        >>> p = i.prompt_constructor.create_memory_prompt("q1")
        >>> p.text.strip().replace("\\n", " ").replace("\\t", " ")
        'Before the question you are now answering, you already answered the following question(s):          Question: Do you like school?  Answer: Prior answer'
        """
        return self.memory_plan.get_memory_prompt_fragment(
            question_name, self.current_answers
        )

    def construct_system_prompt(self) -> Prompt:
        """Construct the system prompt for the LLM call."""
        import warnings

        warnings.warn(
            "This method is deprecated. Use get_prompts instead.", DeprecationWarning
        )
        return self.get_prompts()["system_prompt"]

    def construct_user_prompt(self) -> Prompt:
        """Construct the user prompt for the LLM call."""
        import warnings

        warnings.warn(
            "This method is deprecated. Use get_prompts instead.", DeprecationWarning
        )
        return self.get_prompts()["user_prompt"]

    def get_prompts(self) -> Dict[str, Prompt]:
        """Get both prompts for the LLM call.

        >>> from edsl import QuestionFreeText
        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> q = QuestionFreeText(question_text="How are you today?", question_name="q_new")
        >>> i = InvigilatorBase.example(question = q)
        >>> i.get_prompts()
        {'user_prompt': ..., 'system_prompt': ...}
        """
        prompts = self.prompt_plan.get_prompts(
            agent_instructions=self.agent_instructions_prompt,
            agent_persona=self.agent_persona_prompt,
            question_instructions=self.question_instructions_prompt,
            prior_question_memory=self.prior_question_memory_prompt,
        )
        if len(self.question_image_keys) > 1:
            raise ValueError("We can only handle one image per question.")
        elif len(self.question_image_keys) == 1:
            prompts["encoded_image"] = self.scenario[
                self.question_image_keys[0]
            ].encoded_image

        return prompts

    def _get_scenario_with_image(self) -> Scenario:
        """This is a helper function to get a scenario with an image, for testing purposes."""
        from edsl import Scenario

        try:
            scenario = Scenario.from_image("../../static/logo.png")
        except FileNotFoundError:
            scenario = Scenario.from_image("static/logo.png")
        return scenario


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
