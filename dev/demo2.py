import streamlit as st
from datetime import datetime

import functions
import time
input_article = None
if "length" not in st.session_state:
    st.session_state.length = "700"
    st.session_state.style = False
    st.session_state.chosen_topics = None
    st.session_state.topics = None
    st.session_state.article = None

st.set_page_config(
    page_title="Newsroom.ai Demo",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Using "with" notation
with st.sidebar:

    st.header("Article Parameters")
    st.radio(
        "Choose the length of the article",
        options=["500", "700", "1000"],
        key="length",
    )
    st.checkbox('Trending Topics Style', key='style')

    st.subheader("Selected Topics Variant")
    if st.session_state.chosen_topics:
        st.write(st.session_state.chosen_topics)
    else:
        st.write('No topics selected')

    generate_article_button = st.button(
        'Create Article', disabled=(st.session_state.chosen_topics is None))

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

        with st.spinner('Generating article...'):
            article = functions.article_with_topics(
                input_article, st.session_state.chosen_topics, params)
        st.success("Article is created! You can find it in the Output tab.")

        st.session_state['article'] = article

tab1, tab2 = st.tabs(["Input", "Output"])


with tab1:

    topics_state = False
    col1, col2 = st.columns(2)

    # ----------- Input article ------------

    with col1:
        st.subheader("Input Text")
        st.text('Place for the text/article you want to generate topics for.')
        input_article = st.text_area(
            '', 'Write your article here. You can use Markdown syntax.', height=600, label_visibility='collapsed')

        generate_topics_button = st.button('Create topics')

        if generate_topics_button and input_article:
            with st.spinner('Generating topics...'):
                st.session_state['topics'] = functions.find_topics(
                    input_article)
            st.success("Done!")

    # ----------- Generated Topics ------------

    with col2:
        if st.session_state.topics:
            st.subheader("Generated Topics:")
            st.text('Here you can edit every section with topics and select the one you like the most.\nPlease, click twice on the button to select the topics you want to use for the article generation.')

            for i in range(len(st.session_state.topics)):
                topics_text = st.text_area(
                    '', st.session_state.topics[i], height=300, label_visibility='collapsed')
                if st.button(f'Click twice! - Variant {i+1}'):
                    st.session_state['chosen_topics'] = topics_text


with tab2:
    st.subheader("Generated Article")

    print(f'Topics: {st.session_state.chosen_topics}', end='\n\n')
    print(f'Article: {st.session_state.article}', end='\n\n')

    if st.session_state.article:
        st.text(
            'Here you can see the generated article. You can also download it and edit right here. Enjoy!')
        article_area = st.text_area('', st.session_state.article,
                                    height=600, label_visibility='collapsed')

        timestamp = 1625309472.357246
        date_time = datetime.fromtimestamp(timestamp)
        str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
        print("Current timestamp", str_date_time)

        name = f"{int(time.time())}-{st.session_state.length}-style{st.session_state.style}-{input_article.replace(',', ' ').split()[0]}.txt"
        st.download_button(f'Download {name}', article_area, file_name=name)
    else:
        st.write('No article generated yet')
