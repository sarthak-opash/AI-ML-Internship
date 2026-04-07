from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv() 

prompt1 = PromptTemplate( 
    template = 'Write a joke about {topic}',
    input_variables=['topic'] )

model = ChatGroq(model="llama-3.1-8b-instant")

prompt2 =  PromptTemplate( 
    template = 'explain me the {topic}',
    input_variables=['topic'] )

parser = StrOutputParser()

chain = RunnableSequence(prompt1, model, parser, prompt2, model, parser)
print(chain.invoke({'topic': "AI Engineer"}))