# pocketgroq/chain_of_thought/cot_manager.py

from typing import List, Optional
from .llm_interface import LLMInterface
from .utils import sanitize_input, validate_cot_steps
import logging

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChainOfThoughtManager:
    """
    Manages the Chain-of-Thought reasoning process with enhanced prompting
    to ensure robustness, precision, and efficiency.
    """

    def __init__(self, llm: LLMInterface, cot_prompt_template: Optional[str] = None):
        """
        Initialize with an LLM instance and an optional CoT prompt template.

        Args:
            llm (LLMInterface): An instance of a class that implements the LLMInterface.
            cot_prompt_template (str, optional): Custom template for generating CoT prompts.
                                                  If None, a default robust template is used.
        """
        self.llm = llm
        self.cot_prompt_template = cot_prompt_template or self._default_cot_prompt()
        logger.debug("Initialized ChainOfThoughtManager with custom prompt template.")

    def _default_cot_prompt(self) -> str:
        """
        Provides a robust default Chain-of-Thought prompt template.

        Returns:
            str: The default prompt template.
        """
        return (
            "You are an expert problem solver. Carefully analyze the following problem and provide a detailed, step-by-step reasoning process leading to the solution.\n\n"
            "Problem: {problem}\n\n"
            "Solution Steps:"
        )

    def generate_cot(self, problem: str) -> List[str]:
        """
        Generate intermediate reasoning steps (Chain-of-Thought) for the given problem.

        Args:
            problem (str): The problem statement to solve.

        Returns:
            List[str]: A list of reasoning steps.
        """
        sanitized_problem = sanitize_input(problem)
        prompt = self.cot_prompt_template.format(problem=sanitized_problem)
        logger.debug(f"Generated prompt for CoT: {prompt}")

        response = self.llm.generate(prompt)
        logger.debug(f"Received response from LLM: {response}")

        cot_steps = self._parse_cot(response)
        logger.info(f"Generated {len(cot_steps)} reasoning steps.")

        # Validate the extracted CoT steps
        if not validate_cot_steps(cot_steps):
            logger.warning("Validation failed for the extracted CoT steps.")
            raise ValueError("Invalid Chain-of-Thought steps extracted from LLM response.")

        return cot_steps

    def synthesize_response(self, cot_steps: List[str]) -> str:
        """
        Synthesize the final answer from the Chain-of-Thought steps.

        Args:
            cot_steps (List[str]): A list of reasoning steps.

        Returns:
            str: The final synthesized answer.
        """
        synthesis_prompt = (
            "Based on the following detailed reasoning steps, provide a clear and concise answer to the original problem.\n\n"
            "Reasoning Steps:\n"
            + "\n".join([f"{idx + 1}. {step}" for idx, step in enumerate(cot_steps)]) +
            "\n\nAnswer:"
        )
        logger.debug(f"Synthesis prompt: {synthesis_prompt}")

        final_response = self.llm.generate(synthesis_prompt, max_tokens=200)
        logger.debug(f"Received synthesized answer: {final_response}")

        answer = final_response.strip()

        # Basic validation to ensure an answer was generated
        if not answer:
            logger.error("No answer generated during synthesis.")
            raise ValueError("Failed to generate a synthesized answer from CoT steps.")

        return answer

    def solve_problem(self, problem: str) -> str:
        """
        Complete process to solve a problem using Chain-of-Thought.

        Args:
            problem (str): The problem statement to solve.

        Returns:
            str: The final answer to the problem.
        """
        logger.info(f"Solving problem: {problem}")
        try:
            cot = self.generate_cot(problem)
            answer = self.synthesize_response(cot)
            logger.info("Problem solved successfully.")
            return answer
        except Exception as e:
            logger.error(f"An error occurred while solving the problem: {e}")
            raise

    def _parse_cot(self, response: str) -> List[str]:
        """
        Parse the LLM response to extract individual reasoning steps.
        Enhanced to handle various formatting styles for robustness.

        Args:
            response (str): The raw response from the LLM.

        Returns:
            List[str]: A list of extracted reasoning steps.
        """
        steps = []
        logger.debug("Parsing Chain-of-Thought steps from response.")

        # Attempt to parse numbered or bulleted lists
        lines = response.split('\n')
        for line in lines:
            # Match patterns like "1. Step one" or "- Step one" or "* Step one"
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '-', '*')):
                # Remove leading numbering or bullets
                step = line.strip().lstrip('1234567890.').lstrip('-*').strip()
                if step:
                    steps.append(step)
            else:
                # If no clear list formatting, consider the entire response as a single step
                if not steps and line.strip():
                    steps.append(line.strip())

        logger.debug(f"Extracted steps: {steps}")
        return steps
