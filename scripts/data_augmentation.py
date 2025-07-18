import random
import json
from typing import List, Dict
from .analysis import analyze_conversation

def augment_conversation(conversation: List[Dict], num_variants: int = 3) -> List[List[Dict]]:
    """Генерация вариантов переписки на основе исходной"""
    augmented = []
    for _ in range(num_variants):
        variant = []
        for message in conversation:
            # Простая аугментация: замена синонимов в 30% сообщений
            if random.random() < 0.3:
                new_msg = replace_synonyms(message['text'])
                variant.append({"from": message['from'], "text": new_msg})
            else:
                variant.append(message.copy())
        augmented.append(variant)
    return augmented

def replace_synonyms(text: str) -> str:
    """Замена слов на синонимы (упрощённая версия)"""
    synonyms = {
        "привет": ["здравствуй", "добрый день", "приветствую"],
        "как дела": ["как жизнь", "как поживаешь", "как сам"],
        "нормально": ["хорошо", "отлично", "прекрасно"],
        # Добавьте другие слова по необходимости
    }
    words = text.split()
    new_words = []
    for word in words:
        low_word = word.lower()
        if low_word in synonyms and random.random() < 0.5:
            new_words.append(random.choice(synonyms[low_word]))
        else:
            new_words.append(word)
    return " ".join(new_words)

def annotate_with_llm(conversation):
    """Заглушка для аннотации, так как Groq API недоступен"""
    return {
        "success_chance": 0.5,
        "initiative": "unknown",
        "problems": ["Пример проблемы"],
        "advice": "Пример совета"
    }

if __name__ == "__main__":
    # Пример использования
    with open("cleaned_messages.json", "r", encoding="utf-8") as f:
        original_conv = json.load(f)
    
    # Аугментация
    augmented_convs = augment_conversation(original_conv)
    
    # Сохранение аугментированных данных
    with open("augmented_conversations.json", "w", encoding="utf-8") as f:
        json.dump(augmented_convs, f, ensure_ascii=False, indent=2)
    
    # Разметка (пример для первого варианта)
    for conv in augmented_convs:
        annotation = annotate_with_llm(conv)
        if annotation is None or annotation == {}:
            print("Не удалось аннотировать переписку")
        else:
            print("Разметка:", annotation)
