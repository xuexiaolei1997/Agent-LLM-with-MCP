# LLM with MCP

## Prepare

`touch .env`

update .env

```env
BASE_URL="your chat model"
API_KEY="your api key"
MODEL="your model name"
```

## Install Python

`pip install -r requirements.txt`

## Init node

`npm init -y`

`npm install @modelcontextprotocol/sdk @anthropic-ai/sdk dotenv`

`npm install -D typescript @types/node`

`npx tsc --init`

### update packages.json

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node build/client.js"
  }
}
```

### update tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}
```
