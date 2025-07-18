import json
import requests
from config import GROQ_API_KEY
from .image_processor import extract_text_from_image
from .data_loader import transform_messages

def analyze_with_groq(messages):
    """Отправка структурированного промпта в Groq API для анализа в формате JSON"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Llama-3-8b-8192",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500,
        "response_format": {"type": "json_object"}
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Ошибка API: {response.status_code}, {response.text}")
        return None

def analyze_conversation(conversation):
    """Анализ одной переписки с помощью LLM"""
    # Обработка изображений в сообщениях
    for msg in conversation['messages']:
        if 'image_path' in msg:
            # Обработка изображения
            try:
                text_from_image = extract_text_from_image(msg['image_path'])
                msg['text'] += f"\n[Изображение содержит текст: {text_from_image}]"
            except Exception as e:
                print(f"Ошибка обработки изображения: {e}")
    
    # Преобразуем сообщения в универсальный формат
    transformed_messages = transform_messages(conversation)
    
    # Формируем промпт
    messages = [
        {
            "role": "system",
            "content": "Ты эксперт по психологии общения. Проанализируй переписку из дейтинг-приложения и оцени: 1) вероятность успеха знакомства (success_chance), 2) кто проявляет инициативу (initiative), 3) проблемные моменты общения (problems), 4) дай советы, как улучшить диалог (advice). Ответ дай строго в формате JSON с ключами: success_chance, initiative, problems, advice."
        },
        {
            "role": "user",
            "content": f"Вот переписка в JSON формате:\n{json.dumps(transformed_messages, ensure_ascii=False)}"
        }
    ]
    
    # Отправляем в Groq
    analysis_result = analyze_with_groq(messages)
    if analysis_result is None:
        return None
    try:
        result_json = json.loads(analysis_result)
        print(f"Анализ переписки {conversation['id']}:\n{json.dumps(result_json, indent=2, ensure_ascii=False)}")
        return result_json
    except json.JSONDecodeError:
        print(f"Ошибка парсинга JSON: {analysis_result}")
        return None
