import textwrap
from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from controlflow.llm.models import BaseChatModel
from controlflow.utilities.general import ControlFlowModel, unwrap


class LLMRules(ControlFlowModel):
    """
    LLM rules let us tailor DAG compilation, message generation, tool use, and
    other behavior to the requirements of different LLM provider APIs.

    Rules can be added here (to the base class) and overridden in subclasses, if
    necessary.
    """

    model: Optional[BaseChatModel]

    # require at least one non-system message
    require_at_least_one_message: bool = False

    # system messages can only be provided as the very first message in a thread
    require_system_message_first: bool = False

    # other than a system message, the first message must be from the user
    require_user_message_after_system: bool = False

    # the last message in a thread can't be from an AI if tool use is allowed
    allow_last_message_from_ai_when_using_tools: bool = True

    # consecutive AI messages must be separated by a user message
    allow_consecutive_ai_messages: bool = True

    # add system messages to identify speakers in multi-agent conversations
    # (some APIs can use the `name` field for this purpose, but others can't)
    add_system_messages_for_multi_agent: bool = False

    # if a tool is used, the result must follow the tool call immediately
    tool_result_must_follow_tool_call: bool = True

    # the name associated with a message must conform to a specific format
    require_message_name_format: Optional[str] = None

    def model_instructions(self) -> Optional[list[str]]:
        pass


class OpenAIRules(LLMRules):
    require_message_name_format: str = r"[^a-zA-Z0-9_-]"

    model: ChatOpenAI

    def model_instructions(self) -> list[str]:
        instructions = []
        if self.model.model_name.endswith("gpt-4o-mini"):
            instructions.append(
                unwrap(
                    """
                    You can only provide a single result for each task, and a
                    task can only be marked successful one time. Do not make
                    multiple tool calls in parallel to supply multiple results
                    to the same task.                    
                    """
                )
            )
        return instructions


class AnthropicRules(LLMRules):
    require_at_least_one_message: bool = True
    require_system_message_first: bool = True
    require_user_message_after_system: bool = True
    allow_last_message_from_ai_when_using_tools: bool = False
    allow_consecutive_ai_messages: bool = False


def rules_for_model(model: BaseChatModel) -> LLMRules:
    if isinstance(model, (ChatOpenAI, AzureChatOpenAI)):
        return OpenAIRules(model=model)
    elif isinstance(model, ChatAnthropic):
        return AnthropicRules(model=model)
    else:
        return LLMRules(model=model)
