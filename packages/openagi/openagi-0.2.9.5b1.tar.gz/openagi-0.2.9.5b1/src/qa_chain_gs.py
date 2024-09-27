from typing import List
from genflow import CustomComponent
from langchain.llms.base import BaseLLM
from langchain.schema import Document
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

class QuestionGeneratorChain(CustomComponent):
    display_name: str = "QuestionGeneratorChain"
    description: str = "Generate questions based on a list of documents"
    documentation: str = "https://docs.aiplanet.com/components/chains#questiongeneratorchain"
    beta: bool = False

    def build_config(self):
        return {
            "documents": {"display_name": "Documents"},
            "llm": {"display_name": "LLM"},
            "num_questions": {"display_name": "Number of Questions", "input_types": ["Input"]},
            "system_prompt": {
                "display_name": "Question Generation Prompt",
                "info": "Prompt template for generating questions.",
            },
            "code": {"show": True},
        }

    def validate(self, num_of_questions: int):
        if num_of_questions > 50:
            return "The limit of max number of questions is 50. Please try again with less than 50 questions"
        elif num_of_questions < 5:
            return "The minimum number of questions to generate is 5. Please try again with more than 5 questions"
        return None

    def distribute_evenly(self, num: int, doc_count: int) -> List[int]:
        base_value = num // doc_count
        remainder = num % doc_count
        distribution = [base_value] * doc_count

        for i in range(remainder):
            distribution[i] += 1

        return distribution

    def build(
        self,
        llm: BaseLLM,
        documents: List[Document],
        num_questions: str,
        system_prompt: SystemMessagePromptTemplate,
    ) -> List[Document]:

        try:
            num_questions_int = int(num_questions)
        except ValueError:
            return [Document(page_content="Invalid input for number of questions. Please enter a valid integer.")]

        feedback = self.validate(num_questions_int)
        output: List[Document] = []

        if feedback is None:
            question_distribution = self.distribute_evenly(num_questions_int, len(documents))

            for doc, num_qs in zip(documents, question_distribution):
                if num_qs != 0:
                    template = ChatPromptTemplate.from_messages(
                        [
                            SystemMessage(
                                content=system_prompt.prompt.template.format(
                                    context=doc.page_content,
                                    num_questions=str(num_qs)
                                )
                            )
                        ]
                    )

                    response = llm(template.messages)
                    generated_questions = response.content
                    output.append(Document(page_content=generated_questions, metadata=doc.metadata))
        else:
            output.append(Document(page_content=feedback))

        return output