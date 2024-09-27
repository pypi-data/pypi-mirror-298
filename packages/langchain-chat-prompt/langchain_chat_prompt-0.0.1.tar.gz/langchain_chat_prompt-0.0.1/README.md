# Langchain prompt engineering based on openAi

```
Package: langchain_chat_prompt
```

## Dependencies:

- **Langchain**
- **express**
- **langchain_openai**

## How to use ?

Install the package

pip install langchain_chat_prompt

```python
    #main.py
    from langchain_chat_prompt import OpenaiChatPrompt

    template = """
     Greet {user_name} and ask for address {address}
    """

    actual_data = {
        "user_name": "Bob hamal", "address": "you live"
    }

    dynamic_vars = ['user_name', 'address']

    api_key = 'api_key'

    response = OpenaiChatPrompt.run()
            prompt_response = OpenaiChatPrompt()
    prompt_response.run(dynamic_var=dynamic_vars, data=actual_data, question=actual_data,
                        api_key=api_key, template=template)

```

Run the application using

    python main.py

## Package details description(Parameters)

- ### dynamic_var

  - This will contains those template variables uses, and should be arrays of strings

- ### data

  - Data contains value of the template dynamic variables

- ### question

  - Question you want to know about

- ### api_key

  - Openai api key

- ### template
  - According to template we write
  - We will get response as per template
