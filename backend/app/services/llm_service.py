import ollama
import openai
import google.generativeai as genai
import json
import re
from functools import lru_cache
from app.core.config import settings


class LlmException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class AiService:
    def __init__(self):
        pass

    def get_tasks(self, prompt: str) -> list[dict]:
        return []

    def get_summary(self, project_data: dict) -> str:
        return "This is a dummy summary."

    def ask_question(self, project_data: dict, question: str) -> str:
        return "This is a dummy answer."


class OllamaService(AiService):
    def __init__(self, host="http://127.0.0.1:11434", model="gemma3:1b"):
        super().__init__()
        self.model = model
        self.host = host
        self.client = ollama.Client(host=host)

    def get_tasks(self, prompt: str) -> list[dict]:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a project manager. Your task is to break down an objective into a list of tasks. Return the tasks as a JSON array of objects with the following keys: id, title, description.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                format="json",
            )
        except Exception as e:
            raise LlmException("Ollama API error: " + e)

        tasks_json = json.loads(response["message"]["content"])
        tasks = [tasks_json] if "tasks" not in tasks_json else tasks_json["tasks"]
        return tasks

    def get_summary(self, project_data: dict) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a project manager. Your task is to provide a summary of the project status. Return the summary as a single string in Markdown format.",
                    },
                    {
                        "role": "user",
                        "content": json.dumps(project_data),
                    },
                ],
            )
        except Exception as e:
            raise LlmException("Ollama API error: " + e)

        return response["message"]["content"]

    def ask_question(self, project_data: dict, question: str) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a project manager. Your task is to answer questions about the project based on the provided data. Answer in Markdown format.",
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{json.dumps(project_data)}\n\nQuestion: {question}",
                    },
                ],
            )
        except Exception as e:
            raise LlmException("Ollama API error: " + e)

        return response["message"]["content"]


class OpenAIService(AiService):
    def __init__(
        self,
        base_url="http://localhost:8012/v1/",
        model="gemma-3-1b-it-Q2_K.gguf",
        api_key="llama",
    ):
        super().__init__()
        self.base_url = base_url
        self.model = model
        self.api_key = api_key
        openai.base_url = base_url
        openai.api_key = self.api_key

    def get_tasks(self, prompt: str) -> list[dict]:
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a project manager. Break down the objective into a list of tasks. "
                            "Return ONLY a **valid JSON array** of objects with id, title, description. "
                            "Make sure each object is comma-separated except for the last item, and the output is valid JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                response_format="json",
            )
        except Exception as e:
            raise LlmException("OpenAI API error: " + str(e))

        try:
            content = response.choices[0].message.content
            match = re.search(r"```json\s*(\[.*?\])\s*```", content, re.DOTALL)
            if match:
                json_str = match.group(1)
                try:
                    tasks = json.loads(json_str)
                    return tasks
                except json.JSONDecodeError as e:
                    raise LlmException("Failed to parse JSON:" + e)
            else:
                raise LlmException("No JSON block found.")
        except (KeyError, json.JSONDecodeError) as e:
            raise LlmException("Failed to parse OpenAI response: " + str(e))

    def get_summary(self, project_data: dict) -> str:
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a project manager. Your task is to provide a summary of the project status. Return the summary as a single string in Markdown format.",
                    },
                    {
                        "role": "user",
                        "content": json.dumps(project_data),
                    },
                ],
            )
        except Exception as e:
            raise LlmException("OpenAI API error: " + str(e))

        return response.choices[0].message.content

    def ask_question(self, project_data: dict, question: str) -> str:
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a project manager. Your task is to answer questions about the project based on the provided data. Answer in Markdown format.",
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{json.dumps(project_data)}\n\nQuestion: {question}",
                    },
                ],
            )
        except Exception as e:
            raise LlmException("OpenAI API error: " + str(e))

        return response.choices[0].message.content


class GeminiService:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model_name = model
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)

    def get_tasks(self, prompt: str) -> list[dict]:
        try:
            system_message = (
                "You are a project manager. Break down the objective into a list of tasks. "
                "Return ONLY a **valid JSON array** of objects with id, title, description. "
                "Ensure it is valid JSON, with commas between objects (except the last one). "
                "Wrap the output in triple backticks and json (```json ... ```)."
            )

            full_prompt = f"{system_message}\n\n{prompt}"
            response = self.model.generate_content(full_prompt)

            content = response.text.strip()

            match = re.search(r"```json\s*(\[\s*{.*?}\s*])\s*```", content, re.DOTALL)
            if match:
                json_str = match.group(1)
                try:
                    tasks = json.loads(json_str)
                    return tasks
                except json.JSONDecodeError as e:
                    raise LlmException("Failed to parse JSON: " + str(e))
            else:
                raise LlmException("No valid JSON block found in Gemini response.")
        except Exception as e:
            raise LlmException("Gemini API error: " + str(e))

    def get_summary(self, project_data: dict) -> str:
        try:
            full_prompt = f"You are a project manager. Your task is to provide a summary of the project status. Return the summary as a single string in Markdown format.\n\n{json.dumps(project_data)}"
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            raise LlmException("Gemini API error: " + str(e))

    def ask_question(self, project_data: dict, question: str) -> str:
        try:
            full_prompt = f"You are a project manager. Your task is to answer questions about the project based on the provided data. Answer in Markdown format.\n\nContext:\n{json.dumps(project_data)}\n\nQuestion: {question}"
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            raise LlmException("Gemini API error: " + str(e))


@lru_cache()
def get_llm_service():
    if settings.LLM_SERVICE == "ollama":
        return OllamaService(host=settings.OLLAMA_API_URL, model=settings.OLLAMA_MODEL)
    if settings.LLM_SERVICE == "openai":
        return OpenAIService(
            base_url=settings.OPENAI_API_URL,
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )
    if settings.LLM_SERVICE == "gemini":
        return GeminiService(settings.GEMINI_API_KEY)
    return AiService()
