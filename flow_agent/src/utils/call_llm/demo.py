from openai import OpenAI
from src.config.env import settings

client = OpenAI(
    base_url=settings.LLM_BASE_URL,
    api_key=settings.ARK_API_KEY,
)


def main() -> None:
    response = client.responses.create(
        model=settings.LLM_MODEL_NAME,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "你是谁",
                    },
                ],
            }
        ],
    )
    print(response)


if __name__ == "__main__":
    main()
