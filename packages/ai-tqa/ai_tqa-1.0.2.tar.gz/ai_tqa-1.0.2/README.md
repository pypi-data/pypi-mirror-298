TextEvaluator использует модель AI-TQA1 Basic для оценки текста и определения наличия в нем плохих слов или выражений. 

Алгоритм автоматически очищает текст от ненужных символов (например, заменяет "я-бло/ко" на "яблоко"), что улучшает точность оценки.

# Поддерживаемые языки:

- Украинский
- Русский

# Установка:

`pip install ai-tqa`

# Использование:

```python
from ai_tqa import TextEvaluator

evaluator = TextEvaluator()

text = "Привет, даун!"

result_with_detail = evaluator.evaluate_text(text, detail=True)
result_without_detail = evaluator.evaluate_text(text, detail=False)

print(f"Результат с деталями: Оценка: {result_with_detail[0]}, Плохие слова: {result_with_detail[1]}")
print(f"Результат без деталей: Оценка: {result_without_detail}")
```

# Контрибьюторы:

- KroZen