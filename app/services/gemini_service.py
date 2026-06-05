from google import genai
from google.genai import errors

from app.core.config import settings

import time


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def summarize_text(text: str):

    print("\nTEXT LENGTH:", len(text))

    # Prevent extremely large prompts
    MAX_INPUT_CHARS = 12000

    if len(text) > MAX_INPUT_CHARS:
        text = text[:MAX_INPUT_CHARS]

    prompt = f"""
    You are an advanced AI document summarization assistant.

    Your task is to create a detailed, informative, multi-paragraph summary.

    STRICT RULES:
    - Write at least TWO FULL paragraphs
    - Minimum 150 words
    - Explain the document thoroughly
    - Mention important topics, technologies, concepts, findings, or responsibilities
    - Include key technical details
    - Continue writing until the summary is comprehensive
    - Do NOT stop after one sentence
    - Do NOT generate a short overview
    - The response must feel like a human-written executive summary
    - Keep the summary professional and readable

    DOCUMENT:
    {text}
    """

    retries = 5

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "temperature": 0.7,
                    "max_output_tokens": 2000
                }
            )

            # SAFELY EXTRACT FULL RESPONSE
            summary = ""

            if response.candidates:

                for candidate in response.candidates:

                    if (
                        candidate.content
                        and candidate.content.parts
                    ):

                        for part in candidate.content.parts:

                            if (
                                hasattr(part, "text")
                                and part.text
                            ):

                                summary += part.text

            summary = summary.strip()

            print("\nFULL SUMMARY:\n")
            print(summary)

            word_count = len(summary.split())

            print("\nSUMMARY WORD COUNT:")
            print(word_count)

            # VALIDATE SUMMARY LENGTH
            if word_count < 80:

                print(
                    f"Summary too short. Retry {attempt + 1}"
                )

                time.sleep(3)

                continue

            return summary

        except errors.ServerError:

            print(
                f"Gemini overloaded. Retry {attempt + 1}"
            )

            time.sleep(5)

        except Exception as e:

            print("\nGEMINI ERROR:\n")
            print(e)

            time.sleep(3)

    return """
    Summary generation temporarily failed because
    the Gemini API is currently overloaded.
    Please try again later.
    """