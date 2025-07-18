import json

def load_conversations(file_path):
    """Загрузка и предобработка JSON-файла переписок"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Базовая очистка данных
        cleaned_data = []
        for conv in data:
            # Фильтрация пустых сообщений
            conv['messages'] = [msg for msg in conv['messages'] if msg.get('text', '').strip()]
            
            if conv['messages']:
                cleaned_data.append(conv)
        
        return cleaned_data
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return []

def transform_messages(conversation):
    """Преобразование структуры сообщений в универсальный формат"""
    transformed = []
    for msg in conversation['messages']:
        transformed.append({
            "author": msg['sender'],
            "message": msg['text']
        })
    return transformed
