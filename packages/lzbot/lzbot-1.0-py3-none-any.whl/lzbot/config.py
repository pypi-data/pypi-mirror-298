from openai import OpenAI
def xunfei_chat(model, message, api_key):
    client = OpenAI(
        api_key=api_key, 
        base_url='https://spark-api-open.xf-yun.com/v1'
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return completion.choices[0].message.content