from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.text_splitter import CharacterTextSplitter
import json
import math


def genMCQ(course_name, no_mcqs, pages, api_key, temperature):
    mcqs = []
    chat = ChatOpenAI(temperature=temperature, openai_api_key=api_key)
    
    lecture_content = [p.page_content for p in pages]
    lecture_content = '\n'.join(lecture_content)
    text_splitter = CharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap  = 200,
        separator= " "
    )
    docs = text_splitter.create_documents([lecture_content])
    no_docs = len(docs)
    
    no_of_mcqs = math.ceil(no_mcqs/no_docs)

    for i in range(no_docs):
        mcq_format = [
            {
                "Question": "MCQ question 1 statement",
                "A": "choice a statement",
                "B": "choice b statement",
                "C": "choice c statement",
                "D": "choice d statement",
                "correct_choice": "only one option should be correct and output A,B,C or D"
            },
            {
                "Question": "MCQ question 2 statement",
                "A": "choice a statement",
                "B": "choice b statement",
                "C": "choice c statement",
                "D": "choice d statement",
                "correct_choice": "only one option should be correct and output A,B,C or D"
            }
        ]
        template="""You are a helpful teaching assistant for the course on {course_name} \
        that helps in creating MCQs after each lecture."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template="""Generate {no_mcqs} MCQs given the lecture content: 
        {lecture}
        Output a python list of MCQs. Example output of few MCQs is as follows.
        {mcq_format}
        Only output list of MCQs and nothing else. Conform to the above format. \
        Make sure that the generated MCQs are correct.
        """
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=chat, prompt=chat_prompt)
        mcqs_ = chain.run(course_name=course_name, no_mcqs=no_of_mcqs, mcq_format=json.dumps(mcq_format), lecture=docs[i].page_content)
        mcqs.extend(json.loads(mcqs_))

    return json.dumps(mcqs)
