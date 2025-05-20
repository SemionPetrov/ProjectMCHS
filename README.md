# ProjectMCHS

[Доки](https://drive.google.com/drive/folders/1O8I7lcUWHXA4Z6xpvW2Tnp-mM9MzI16N)

## Запуск

В *src* исполняем.

```shell
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Очевидно нужен *poetry*

Докер потом сделаю.

Мы остановились на том, что фронт делают на чем хотят и походу в отдельном репозитории.
Следующий шаг это пути api и делать бд.
