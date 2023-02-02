import streamlit as st
import functions

if "length" not in st.session_state:
    st.session_state.length = "700"
    st.session_state.style = False
    st.session_state.chosen_topics = None
    st.session_state.topics = None
    st.session_state.article = None

st.title("Newsroom.ai Demo")

topics_state = False

input_article = st.text_area('Input article', '''
      Write your article here. You can use Markdown syntax.
    ''', height=400)

generate_topics_button = st.button('Create topics')


if generate_topics_button and input_article:
    # TODO: Create st loader
    topics_state = st.text('Generating topics...')
    st.session_state['topics'] = functions.find_topics(input_article)
    topics_state.text('Done!')

if st.session_state.topics:
    st.subheader("Generated Topics:")
    for i in range(len(st.session_state.topics)):
        topics_text = st.text_area(
            '', st.session_state.topics[i], height=400)
        if st.button(f'Select Variant {i+1}'):
            st.session_state['chosen_topics'] = topics_text

st.subheader("Selected Topics Variant")
if st.session_state.chosen_topics:
    st.text(st.session_state.chosen_topics)
else:
    st.text('No topics selected')

st.subheader("Article Parameters")
col1, col2 = st.columns(2)
with col1:
    st.radio(
        "Choose the length of the article",
        options=["500", "700", "1000"],
        key="length",
    )

with col2:
    st.checkbox('Trending Topics Style', key='style')


generate_article_button = st.button('Generate Article')
if generate_article_button and st.session_state.chosen_topics:
    # Regulate parameters
    params = {}
    if (st.session_state.style):
        style = functions.load_json("data/styles.json")['data'][0]['value']
        params = {
            'length': f'{st.session_state.length} words',
            'text-style': str(style)
        }
    else:
        params = {'length': f'{st.session_state.length} words'}

    article_state = st.text('Generating article...')
    article = functions.article_with_topics(
        input_article, st.session_state.chosen_topics, params)
    article_state.text('Done!')

    st.session_state['article'] = article
    st.subheader("Generated Article")

    print(f'Topics: {st.session_state.chosen_topics}', end='\n\n')
    print(f'Article: {st.session_state.article}', end='\n\n')
    st.text_area('', st.session_state.article, height=400)
