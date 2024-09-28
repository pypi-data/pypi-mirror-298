from pydantic import BaseModel, Field

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_upstage import ChatUpstage


# Define your desired data structure.
class Score(BaseModel):
    score: int = Field(
        description="An integer rating from 1 to 5. 1 represents the worst or most negative evaluation, 3 is neutral, and 5 represents the best or most positive evaluation."
    )


def get_judge_score(
    prompt: str,
    answer: str,
    ground_truth_answer: str,
    judge_llm: ChatUpstage = None,
    trials: int = 3,
    criteria: str = ""
) -> int:
    """
    Evaluate the quality of an AI assistant's answer to a given prompt.

    This function uses a language model to assess the quality of an answer
    on a scale of 1 to 5, where 1 is the lowest score and 5 is the highest.

    Args:
        prompt (str): The original question or prompt given to the AI assistant.
        answer (str): The AI assistant's response to be evaluated.
        ground_truth_answer (str): The correct or expected answer, if available.
        judge_llm (ChatUpstage, optional): The language model used for judging.
            If None, a new ChatUpstage instance will be created. Defaults to None.
        trials (int, optional): The number of attempts to get a valid score.
            Defaults to 3.

    Returns:
        int: The evaluation score (1-5), or -1 if unable to obtain a valid score.

    Note:
        The function uses a JSON output parser to ensure the score is returned
        in the correct format. If an exception occurs during evaluation, it will
        retry up to the specified number of trials.
    """
    if judge_llm is None:
        judge_llm = ChatUpstage()

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Score)

    prompt_template = PromptTemplate(
        template="""You are an AI Language Model evaluator tasked with assessing the quality of an AI assistant's response to a user's question.

Instructions:
1. Carefully read the provided prompt, ground truth (if available), and the AI's answer.
2. Evaluate the answer on a scale of 1 to 5:
   - 1: Very poor or incorrect answer
   - 2: Below average, partially incorrect or incomplete
   - 3: Average, mostly correct but could be improved
   - 4: Above average, correct and informative
   - 5: Excellent, comprehensive and accurate

3. Consider the following aspects:
   - Relevance to the prompt
   - Accuracy (especially compared to the ground truth, if provided)
   - Completeness of the answer
   - Clarity and coherence

4. Additional criteria: {criteria}

5. Output your evaluation as a single JSON object with the "score" key.

Example outputs:
{{"score": 3}}
{{"score": 5}}
{{"score": 1}}

Important: Provide only the JSON output, no explanations or additional text.

---
Prompt: {prompt}
Ground Truth: {ground_truth}
---
Answer: {answer}
---
Evaluation (JSON format):
""",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt_template | judge_llm | parser

    for _ in range(trials):
        try:
            score = chain.invoke(
                input={
                    "prompt": prompt,
                    "answer": answer,
                    "ground_truth": ground_truth_answer,
                    "criteria": criteria
                }
            )
            return int(score["score"])
        except Exception as e:
            print(e)
    return -1


class Winner(BaseModel):
    winner: str = Field(description="Select the winer A or B")


def get_winner(
    prompt, A_answer, B_answer, ground_truth_answer, judge_llm=None, trials=3, criteria: str = ""
):
    if judge_llm is None:
        judge_llm = ChatUpstage()

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Score)

    prompt_template = PromptTemplate(
        template="""You are an AI Language Model evaluator tasked with selecting the better answer between two options (A or B) provided by an AI assistant in response to a user's question.

Instructions:
1. Carefully read the provided prompt, ground truth (if available), and both answers (A and B).
2. Evaluate both answers based on the following criteria:
   - Relevance to the prompt
   - Accuracy (especially compared to the ground truth, if provided)
   - Completeness of the answer
   - Clarity and coherence

3. Additional criteria: {criteria}

4. Select the winner (A or B) that best addresses the user's question.
5. Output your decision as a single JSON object with the "winner" key.

Example outputs:
{{"winner": "A"}}
{{"winner": "B"}}

Important: Provide only the JSON output, no explanations or additional text.

---
Prompt: {prompt}
Ground Truth: {ground_truth}
---
Answer A: {A_answer}
---
Answer B: {B_answer}
---
Winner (JSON format):
""",
        input_variables=["prompt", "ground_truth", "A_answer", "B_answer"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt_template | judge_llm | parser

    for _ in range(trials):
        try:
            winner = chain.invoke(
                input={
                    "prompt": prompt,
                    "A_answer": A_answer,
                    "B_answer": B_answer,
                    "ground_truth": ground_truth_answer,
                    "criteria": criteria
                }
            )
            return winner["winner"]
        except Exception as e:
            print(e)
    return -1


def _judgeAB(
    prompt, A_answer, B_answer, ground_truth_answer=None, judge_llm=None, trials=7
):
    if judge_llm is None:
        judge_llm = ChatUpstage()

    for _ in range(trials):
        A_score = get_judge_score(prompt, A_answer, ground_truth_answer, judge_llm)
        B_score = get_judge_score(prompt, B_answer, ground_truth_answer, judge_llm)

        winner = get_winner(prompt, A_answer, B_answer, ground_truth_answer)
        if winner == "A" and A_score > B_score or winner == "B" and B_score > A_score:
            return A_score, B_score

    # Not conclusive
    return 0, 0


def judge(
    prompt: str,
    A_answer: str,
    B_answer: str,
    ground_truth_answer: str = None,
    judge_llm: ChatUpstage = None,
    trials: int = 7,
) -> tuple[int, int]:
    """
    Judge two answers (A and B) based on a given prompt and optional ground truth.

    This function evaluates the consistency and quality of two answers by comparing
    them directly and in reverse order. It returns scores only if the judgments are
    consistent across both comparisons.

    Args:
        prompt (str): The question or context for which the answers are provided.
        A_answer (str): The first answer to be evaluated.
        B_answer (str): The second answer to be evaluated.
        ground_truth_answer (str, optional): The correct answer, if available. Defaults to None.
        judge_llm (ChatUpstage, optional): The language model used for judging. Defaults to None.
        trials (int, optional): The number of attempts for each judgment. Defaults to 7.

    Returns:
        tuple[int, int]: A tuple containing the scores for A and B respectively.
                         Returns (0, 0) if the judgments are inconsistent.

    Note:
        - Scores are summed from two rounds of judgments to provide a more robust evaluation.
        - A score of 0 for both answers indicates either inconsistency or failure to judge.
    """

    def _compare_answers(ans1: str, ans2: str) -> tuple[int, int]:
        return _judgeAB(prompt, ans1, ans2, ground_truth_answer, judge_llm, trials)

    A_score1, B_score1 = _compare_answers(A_answer, B_answer)
    if A_score1 == 0 and B_score1 == 0:
        return 0, 0

    B_score2, A_score2 = _compare_answers(B_answer, A_answer)
    if A_score2 == 0 and B_score2 == 0:
        return 0, 0

    if (A_score1 > B_score1 and A_score2 > B_score2) or (
        B_score1 > A_score1 and B_score2 > A_score2
    ):
        return A_score1 + A_score2, B_score1 + B_score2
    else:
        return 0, 0
