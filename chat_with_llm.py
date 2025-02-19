
def chat_with_llm(prompt, client, username, temperature):
    """
    Interact with the OpenAI API to get a response based on the prompt.
    Args:
        prompt (str): The user prompt.
        client: The OpenAI client.
        username (str): The username for the OpenAI API.
        temperature (float): The temperature for the OpenAI API.
    Returns:
        str: The response from the OpenAI API.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        user=username,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    print(response)
    return response.choices[0].message.content