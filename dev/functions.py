import os
import json
import openai
import streamlit as st


# Set your secret API key
openai.organization = "org-Hw1PKAJUymy5LvLwZdN1q5wj"
openai.api_key = "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"


def load_json(filename):
    with open(filename, "r") as f:
        file_contents = f.read()
    return json.loads(file_contents)


def run_completion(prompt, n=1, max_tokens=2000, temperature=0.7, top_p=1, frequency_penalty=0, presence_penalty=0):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        n=n
    )
    return response

# 1. Find main topics of the article.
# [Article] -> [Main topics]


def find_topics(n_sentence_topic=1, n_topics=5, n_choices=3, input_article: str = None):
    todo_topics = f'Find {n_topics} main topics (up to {n_sentence_topic} sentences each) in the article and organize them as json.'
    # todo_topics = f'Find {n_topics} main topics (up to 10 words per each topic) in the next article and organize them as json.'

    # Form prompt and run completion
    prompt_1 = f'todo: {todo_topics}, article: {input_article}'
    output_1 = run_completion(prompt_1, n_choices)

    # TODO: Validation step - if topics are really good.
    topics = []
    for i in output_1['choices']:
        topics.append(i['text'])

    return topics

# 2. With main topics and input article, generate a new article.
# [Article, Main topics] -> [New article]


def article_with_topics(input_article: str = None, topics: str = None, params: dict = None):
    todo_article = f'Based on the article and topics in this json, write a new article with next parameters: {params} .'

    prompt_2 = f'todo: {todo_article}, article: {input_article}, topics: {topics}'
    print('prompt_2', prompt_2)
    output_2 = run_completion(prompt_2)
    print(output_2['choices'])

    article = output_2['choices'][0]['text']
    return article

# 3. Find the most mindblower fact in the article.


def find_mindblower_fact(input_article: str = None, n_choices: int = 3):
    todo_fact = f'Find the most mindblower fact in the article.'

    prompt = f'todo: {todo_fact}, article: {input_article}'
    output = run_completion(prompt, n_choices)

    facts = []
    for i in output['choices']:
        facts.append(i['text'])

    return facts


def usage():
    # Load article
    input_article = load_json(
        "data/articles.json")['data'][0]['value']

    # Load style
    style = load_json("data/styles.json")['data'][0]['value']

    topics = find_topics(input_article=input_article)

    # Parameters for the article
    params = {
        'length': '700 words',
        # 'text-style': str(style)“
    }

    chosen_topics = topics[1]
    article = article_with_topics(
        input_article=input_article, topics=chosen_topics, params=params)

    print(f'Topics: {chosen_topics}', end='\n\n')
    print(f'Article: {article}', end='\n\n')
