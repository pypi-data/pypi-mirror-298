from cbr_athena.llms.chats.LLM__Platform_Engine import LLM__Platform_Engine
from cbr_athena.llms.providers.groq.LLM__Groq   import LLM__Groq
from cbr_athena.llms.providers.mistral.LLM__Mistral import LLM__Mistral
from cbr_shared.schemas.base_models.chat_threads.LLMs__Chat_Completion import LLMs__Chat_Completion


class LLM__Platform_Engine__Mistral(LLM__Platform_Engine):
    llm_platform       : str
    llm_provider       : str
    llm_model          : str
    llm_chat_completion: LLMs__Chat_Completion
    llm__mistral       : LLM__Mistral

    # def is_provider_available(self):
    #     return False

    def execute_request(self):
        with self.llm__mistral as _:
            _.add_messages__system(self.llm_chat_completion.system_prompts)
            _.add_histories       (self.llm_chat_completion.histories     )
            _.add_message__user   (self.llm_chat_completion.user_prompt   )
            _.set_model           (self.llm_model)
            _.set_stream          (self.llm_chat_completion.stream)
            return _.chat_completion()