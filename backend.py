from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

def chatbot_init(temperature=0.5, top_p=1):
    chatbot_llm = Bedrock(
        credentials_profile_name='default',
        model_id='anthropic.claude-v2:1',
        model_kwargs={
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens_to_sample": 300,
            "stop_sequences": ["\n\nHuman:"],
            "anthropic_version": "bedrock-2023-05-31"
        }, 
        region_name='us-east-1'
    )
    return chatbot_llm

def chatbot_memory():
    # Initialize a new, empty memory buffer
    memory = ConversationBufferMemory(max_token_limit=512)
    return memory

def format_prompt(character_profile, input_text):
    # Add emotional tone based on character profile
    if character_profile.lower() == "mom":
        emotion_tone = "with motherly warmth and understanding."
    elif character_profile.lower() == "dad":
        emotion_tone = "with fatherly guidance and support."
    elif character_profile.lower() == "sibling":
        emotion_tone = "with a mix of playful teasing and support, like a typical sibling."
    elif character_profile.lower() == "significant other":
        emotion_tone = "with love, care, and intimate understanding."
    elif character_profile.lower() == "friend":
        emotion_tone = "in a friendly and casual manner."
    elif character_profile.lower() == "teacher":
        emotion_tone = "with educational insights and encouragement."
    elif character_profile.lower() == "coach":
        emotion_tone = "with motivation and strategic advice."
    else:
        emotion_tone = "in a neutral and informative manner."
    
    formatted_input = f"{input_text} (Respond {emotion_tone}) [/INST]"
    return formatted_input

def chatbot_chain(input_text, character_profile, memory, temperature=0.5, top_p=1):
    llm_conversation = ConversationChain(
        llm=chatbot_init(temperature, top_p),
        memory=memory,
        verbose=True
    )

    # Format the input with character profile emotion
    formatted_input = format_prompt(character_profile, input_text)
    chat_reply = llm_conversation.predict(input=formatted_input)

    return chat_reply