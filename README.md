# LLM with MCP

## Prepare

`touch .env`

update .env

```env
BASE_URL="Your chat model"
API_KEY="Your api key"
MODEL="Your model name"
```

## Install Python

`pip install -r requirements.txt`

## Init node

`npm init -y`

`npm install @modelcontextprotocol/sdk @anthropic-ai/sdk dotenv`

`npm install -D typescript @types/node`

`npx tsc --init`

### Update packages.json

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    // "start": "node build/client.js"
  }
}
```

### Update tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    // "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}
```

## Run

### Config MCP Server in run.py

Edit run.py and change variable `servers_list` what you want to use.

`python run.py`
