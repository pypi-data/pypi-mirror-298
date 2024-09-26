# Python Project

## Usage

```sh
venv/bin/python main.py

curl localhost:7869/api/generate -d '{
	"model": "llama3.1",
	"prompt": "hi",
	"stream": false
}'
```

## Environment

| key             | type   | default                 | description                             |
| --------------- | ------ | ----------------------- | --------------------------------------- |
| HOST            | string | "http://localhost:7869" | base url to the Ollama server           |
| MODEL           | string | "llama3.2"              | default model to use                    |
| KEEP_ALIVE_MINS | int    | 20                      | max time to keep unused model in memory |
