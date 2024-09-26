from openai import AzureOpenAI

def ModelOpenAI(prompt, data, query, api_key, api_version, azure_endpoint, model="gpt-4o-mini", max_tokens=500, limit_response=True):
    """
    Generates a response using Azure OpenAI's chat completions API.

    Args:
        prompt (str): The system's initial message for setting the assistant's behavior.
        data (str): The combined document content provided as context.
        query (str): The user's input or question to be processed.
        api_key (str): Azure OpenAI API key.
        api_version (str): The version of the API to use.
        azure_endpoint (str): The endpoint for the Azure OpenAI service.
        model (str): The model to use for the chat completion (default is "gpt-4o-mini").
        max_tokens (int): The maximum number of tokens for the response (default is 500).
        limit_response (bool): A flag to ensure that the assistant respects the token limit.

    Returns:
        str: The generated response from the assistant.
    """
    try:
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )

        # Modify the prompt to include the max_tokens instruction if limit_response is True
        if limit_response:
            prompt += f"\nNota: Asegúrate de que la respuesta no exceda {max_tokens} tokens. siempre da una respuesta resumida lo mas posbile pero entrega la respuesta completa siempre."

        # Create the chat completion request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{data}\n\nPregunta: {query}"}
            ],
            max_tokens=max_tokens
        )
        # Extract the generated response from the API response
        generated_response = response.choices[0].message.content.strip()

        return generated_response

    except Exception as e:
        # Handle errors and return a meaningful message
        return f"Error during Azure OpenAI API call: {str(e)}"
