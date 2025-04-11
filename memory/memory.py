from langgraph.checkpoint.memory import MemorySaver


def create_memory():
    """
    上下文记忆
    """
    return MemorySaver()
