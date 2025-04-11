from langchain_core.prompts import ChatPromptTemplate


def create_prompt(prompt):
    primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", prompt,
            ),
            ("placeholder", "{messages}"),
        ]
    )
    return primary_assistant_prompt
