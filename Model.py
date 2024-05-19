import langchain
import langchain_openai
import langchain_core
import langchain_community
from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import openai
from langchain_openai import ChatOpenAI


llm = OpenAI(openai_api_key = "**********OPENAI_API_KEY**********", 
             model_name = "gpt-3.5-turbo-instruct", 
             temperature = 0.5,
            max_tokens = 1000)


def sentiment_analysis(user_text):
    """
    Categorizes user text into predefined sentiment categories related to Python programming queries.

    This function takes a piece of user-provided text and classifies it into one of three categories:
    1. Friendly chatting or unclear input.
    2. General Python questions not specific to the user's code.
    3. Specific doubts about the user's code, including issues and modifications.

    Parameters:
    user_text (str): The text provided by the user that needs to be categorized.

    Returns:
    str: The number corresponding to the identified category.

    The function follows these steps:
    1. Constructs a prompt that asks the model to categorize the provided text into one of the predefined categories.
    2. Initializes the language model with specific settings.
    3. Sends the prompt to the model and retrieves the response.
    4. Extracts and returns the category number from the model's response.
    """
    categories = [
        "Friendly chatting with the chat. The user ask the ChatBot about his job. If the input is really unclear, choose this category.",
        "The user asks something general about Python, not specific about the user's code.",
        """Specific doubts about the code in the script, the user explicitly references his code or talks about having an issue. The user can also ask if the
        issue is now correct, refering to modifications it just made on his code.""",
    ]
    
    # Create a prompt to ask the model to categorize the text
    prompt = f"Categorize the following text into one of the following categories:\n"
    prompt += "\n".join([f"{i+1}. {category}" for i, category in enumerate(categories)])
    prompt += f"\n\nText: \"{user_text}\"\n."
    prompt += f"The output should be just the number of the category. For example, for the text: <Who are you?>, the answer should be <1>"
    
    #Charge the model
    chat = ChatOpenAI(
        openai_api_key="**********OPENAI_API_KEY**********",
        model="gpt-3.5-turbo",
        temperature=0
    )

    messages = [
        {"role": "system", "content": """You are a helpful assistant whose role is to classify the input in diferent categories. 
        The input will probably be something about programming."""},
        {"role": "user", "content": prompt}
    ]
    
    response = chat.invoke(messages)
    
    # Extract the category from the response
    category = response.content.strip()
    return category


def conversational_talk(conversation, user_prompt, model = llm):
    """
    Generates a response to a conversational query while ensuring specific words are excluded.

    This function takes the current conversation context and a user prompt to generate a response to a conversational 
    query. It ensures that specific words such as 'AI' and 'System' do not appear in the response. The function updates 
    the conversation context with the user's query and the model's response.

    Parameters:
    conversation (list): The current conversation context as a list of tuples, where each tuple 
                         represents a message (e.g., [("human", "message"), ("ai", "response")]).
    user_prompt (str): The conversational query provided by the user.
    model (object, optional): The language model used for generating the response. Defaults to `llm`.

    Returns:
    str: The generated response to the user's conversational query.

    The function follows these steps:
    1. Constructs a prompt using the current conversation context and the user's query.
    2. Updates the conversation context with the user's query.
    3. Invokes the language model to generate a response, ensuring certain words are excluded.
    4. Cleans up the response by removing any unnecessary prefixes.
    5. Updates the conversation context with the model's response.
    """
    prompt_template = ChatPromptTemplate.from_messages(
        conversation  + [("human", "It is essential that the words 'AI', 'System' or similar, do not appear in your answer. Answer the following user query: {question}.")]
    )

    prompt = prompt_template.format_messages(question = user_prompt)

    print(prompt[-1].content)

    conversation += [("human", prompt[-1].content)]
    
    output = model.invoke(prompt)
    output = output.replace("AI:","")
    output = output.replace("System:","")
    output = output.lstrip("\n")

    conversation += [("ai", output)]

    return output


def general_Python_talk(conversation, user_prompt, model = llm):
    """
    Generates a response to a general Python-related question.

    This function takes the current conversation context and a user prompt to generate a response to a general 
    Python-related question. It updates the conversation context with the user's query and the model's response.

    Parameters:
    conversation (list): The current conversation context as a list of tuples, where each tuple 
                         represents a message (e.g., [("human", "message"), ("ai", "response")]).
    user_prompt (str): The general Python-related question provided by the user.
    model (object, optional): The language model used for generating the response. Defaults to `llm`.

    Returns:
    str: The generated response to the user's Python-related question.

    The function follows these steps:
    1. Constructs a prompt using the current conversation context and the user's question.
    2. Updates the conversation context with the user's query.
    3. Invokes the language model to generate a response.
    4. Cleans up the response by removing any unnecessary prefixes.
    5. Updates the conversation context with the model's response.
    """
    prompt_template = ChatPromptTemplate.from_messages(
        conversation  + [("human", "Respond to the question: {question}")]
    )

    prompt = prompt_template.format_messages(question = user_prompt)

    conversation += [("human", prompt[-1].content)]
    
    output = model.invoke(prompt)
    output = output.replace("AI:","").replace("System:","").lstrip("\n")

    conversation += [("ai", output)]
    
    return output


def specific_Python_talk(conversation, user_prompt, user_code, model = llm):
    """
    Generates a detailed and professional response to a specific Python-related query.

    This function is designed to interact with another expert in Python. It takes the current conversation context,
    a user prompt, and a piece of user-provided code to generate a detailed response. The response includes an 
    explanation of the code and answers any specific questions about it. If the user explicitly asks whether the code 
    is correct, the function will also address this.

    Parameters:
    conversation (list): The current conversation context as a list of tuples, where each tuple 
                         represents a message (e.g., [("human", "message"), ("ai", "response")]).
    user_prompt (str): The specific question or query provided by the user.
    user_code (str): The Python code provided by the user for analysis.
    model (object, optional): The language model used for generating the response. Defaults to `llm`.

    Returns:
    str: A detailed response including an explanation of the code and any necessary modifications.

    The function follows these steps:
    1. Generates an initial explanation of the provided code using a predefined system prompt.
    2. Constructs a detailed prompt that includes the initial explanation and the user's specific query.
    3. Updates the conversation context with the user's query and the generated prompt.
    4. Invokes the language model to generate a detailed response.
    5. Cleans up the response by removing any unnecessary prefixes.
    6. Updates the conversation context with the model's response.
    """

    explainer_system_prompt = """You are an expert Python developer. You are able to provide detailed solutions, 
    advice and clear explanations of complex programming issues. You should respond in a concise and professional manner. 
    You are talking with another expert, so use as much technical vocabulary as you want. The format of you're answer 
    should be directly text, never start with \nAI, \nSystem or similar."""

    explanation_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", explainer_system_prompt),
            ("human", """Provide a short summary about the code: {code}. The format of the output should be:
            This code performs the following tasks <Explanation>""")
        ]
    )

    explanation_chain = (
        explanation_prompt_template 
        | model 
        | {"response": RunnablePassthrough() | StrOutputParser()})

    explanation = explanation_chain.invoke(user_code)

    prompt_template = ChatPromptTemplate.from_messages(
        conversation  + [("human", """We have the following code {code}. {explanation}. Answer the question about it: "{question}". Take into account what we have talked about
                          the code previously. 
                          Always mention any change you make in the original code. The output should be given in the following format:
                          <If and only if the user asks explicitaly wether his code is correct, say wether the code is correct or not.>
                          Explanation: 
                          <Short explanation of the code.>
                          New version of the code:
                          <The new version of the code>""")]
    )

    prompt = prompt_template.format_messages(code = user_code, 
                                             explanation = explanation["response"], 
                                             question = user_prompt)

    conversation += [("human", prompt[-1].content)]

    output = model.invoke(prompt)
    output = output.replace("AI:","").replace("System:","").lstrip("\n")

    conversation += [("ai", output)]
    
    return output


def code_analysis(conversation, user_code, model = llm):
    """
    Analyzes and explains a given piece of code, suggesting improvements if necessary.

    This function generates a prompt to analyze and explain the provided code. It identifies any issues
    or clear improvements, focusing on enhancing the code without adding new functionality. The analysis 
    is then added to the conversation context and returned.

    Parameters:
    conversation (list): The current conversation context as a list of tuples, where each tuple 
                         represents a message (e.g., [("human", "message"), ("ai", "response")]).
    user_code (str): The code provided by the user for analysis.
    model (object, optional): The language model used for generating the analysis and response. Defaults to `llm`.

    Returns:
    str: The generated explanation and possible improvements of the provided code.
    """
    prompt_template = ChatPromptTemplate.from_messages(
        conversation  + [("human", """Analize and explain the following code: {code}. If and only if you think there is any issues or clear 
        improvements, give a list of them. The improvements should focus on doing what the user wants to do, but better, 
        not adding new functionality. The output should be given in the following format:
        Explanation: 
        <The explanation of the code>
        Possible improvement:
        <A numbered list of the possible improvements>""")]
    )

    prompt = prompt_template.format_messages(code = user_code)
    
    output = model.invoke(prompt)
    output = output.replace("AI:","").replace("System:","").lstrip("\n")

    conversation += [("ai", output)]
    
    return output


def generate_answer(conversation, text, user_code, model = llm):
    """
    Generates a response based on user input and context.

    This function analyzes the provided text to determine the appropriate response category.
    It then generates a response using different functions based on the category of the input text.
    If no text is provided, it defaults to analyzing the provided code.

    Parameters:
    conversation (list): The current conversation context as a list of tuples, where each tuple 
                         represents a message (e.g., [("human", "message"), ("ai", "response")]).
    text (str): The user's input text.
    user_code (str): The code provided by the user for analysis.
    model (object, optional): The language model used for generating responses. Defaults to `llm`.

    Returns:
    str: The generated response based on the input text and context.

    The function follows these steps:
    1. Checks if the user has provided input text.
    2. Uses sentiment analysis to categorize the input text.
    3. Based on the category, generates a response using one of the following functions:
       - conversational_talk: For friendly chatting or unclear input.
       - general_Python_talk: For general Python-related questions.
       - specific_Python_talk: For specific doubts about the user's code.
    4. If no text is provided, defaults to code analysis using the code_analysis function.
    """
    if text != "": 
        category = sentiment_analysis(text)
        print(category)
        if category == "1":
            answer = conversational_talk(conversation = conversation, user_prompt = text, model = model)
            return answer
        elif category == "2":
            answer = general_Python_talk(conversation = conversation, user_prompt = text, model = model)
            return answer
        else:
            answer = specific_Python_talk(conversation = conversation, user_prompt = text, user_code = user_code, model = model)
            return answer
    else:
        answer = code_analysis(conversation = conversation, user_code = user_code, model = model)
        return answer