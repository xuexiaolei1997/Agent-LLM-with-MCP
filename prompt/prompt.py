from langchain_core.prompts import ChatPromptTemplate


def create_prompt(prompt):
    """提示词模板

    Args:
        prompt (str): 提示词

    Returns:
        _type_: 构建好的提示词
    """
    primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", prompt,
            ),
            ("placeholder", "{messages}"),
        ]
    )
    return primary_assistant_prompt
