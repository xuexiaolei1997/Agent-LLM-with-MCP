# LLM with MCP

## Prepare

`touch .env`

Update .env to use LLM

```env
BASE_URL="Your chat model"
API_KEY="Your api key"
MODEL="Your model name"
```

## Python Environment

Install python>=3.10 and install packages using command below:

`pip install -r requirements.txt`

## Node Environment

Install Node.js>=20 and using command `node -v`, `npm -v` to make sure installed nodejs correctly.

`cd /{workdir}`

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
