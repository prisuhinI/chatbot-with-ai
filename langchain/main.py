import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []


def get_text():
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                               placeholder="Hello! Write your question here: ",
                               label_visibility='hidden')
    return input_text


# Define Function to start a new chat
def new_chat():
    save = []

    for j in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state['past'][j])
        save.append('Bot:' + st.session_state['generated'][j])
    st.session_state['stored_session'].append(save)
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['input'] = ""
    st.session_state.entity_memory.entity_store = {}
    st.session_state.entity_memory.buffer.clear()


st.title("Memory Bot")

# API
api = st.sidebar.text_input("API-key", type="password")
# api = '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'
model = st.sidebar.selectbox(label="Choose model", options=['gpt-3.5-turbo', 'gpt-3.5-turbo-0301', 'text-davinci-003'])

if api:
    # Create Open AI  instance
    llm = OpenAI(
        temperature=0,
        openai_api_key=api,
        model_name=model,
    )

    # Create conv memory
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=10)

    # Create the Conversation Chain
    conversation = ConversationChain(
        llm=llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory
    )
else:
    st.error("No API found")
st.sidebar.button("New Chat", on_click=new_chat, type='primary')

# Get the user input
user_input = get_text()

# Generate the output
if user_input:
    output = conversation.run(input=user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


with st.expander("conversation"):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state['past'][i], icon="👨‍🍳")
        st.success(st.session_state["generated"][i], icon='🤖')
