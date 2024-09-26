import logging

from dria_workflows import WorkflowBuilder, Operator, Edge, Peek, Size, Expression, ConditionBuilder, \
    GetAll, Workflow, Push


def generate_questions(
        input_data: dict,
        max_time: int = 300,
        max_steps: int = 30,
        max_tokens: int = 750
) -> Workflow:
    """Generate questions for a given context and backstory.

    Args:
        input_data (dict): The input data to be used in the workflow.
        max_time (int, optional): The maximum time to run the workflow. Defaults to 300.
        max_steps (int, optional): The maximum number of steps to run the workflow. Defaults to 30.
        max_tokens (int, optional): The maximum number of tokens to use in the workflow. Defaults to 750.

    Returns:
        dict: The generated questions.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    builder = WorkflowBuilder(memory=input_data)

    builder.set_max_time(max_time)
    builder.set_max_steps(max_steps)
    builder.set_max_tokens(max_tokens)

    # Step A: QuestionGeneration
    builder.generative_step(
        id="question_generation",
        path="question.md",
        operator=Operator.GENERATION,
        inputs=[
            Peek.new(index=0, key="context", required=True),
            GetAll.new(key="history", required=False),
            GetAll.new(key="backstory", required=True)
        ],
        outputs=[Push.new("history")]
    )

    flow = [
        Edge(source="question_generation", target="_end", condition=ConditionBuilder.build(
            input=Size.new("history", required=True),
            expression=Expression.GREATER_THAN,
            expected="3",
            target_if_not="question_generation"
        ))
    ]
    builder.flow(flow)
    builder.set_return_value("history")
    workflow = builder.build()

    return workflow

if __name__ == "__main__":
    w = generate_questions({"context":"context", "backstory":["backstory1", "backstory2", "backstory3"]})
    print(w)