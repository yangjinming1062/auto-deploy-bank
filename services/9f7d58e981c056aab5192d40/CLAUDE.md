# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a monorepo containing multiple AWS Generative AI sample projects powered by Amazon Bedrock. Each project is a self-contained solution demonstrating different GenAI use cases.

## Project Categories

### 1. Python Web Applications (Streamlit/Gradio)
Most projects use Streamlit for frontend with Amazon Bedrock integration:
- `app.py` - Main application entry point
- `requirements.txt` - Python dependencies
- Run locally: `pip install -r requirements.txt && streamlit run app.py`

### 2. Serverless/Lambda Projects (Node.js)
`AWS-GenAI-Contact-Center/amazon-connect/` uses Serverless Framework:
- `serverless.yaml` - Infrastructure definition
- `package.json` - Node.js dependencies
- `src/lambda/` - Lambda function handlers (Node.js 18.x)
- Deploy: `./scripts/serverless_deploy.sh <stage>` (requires env config in `env/<stage>.sh`)

### 3. SageMaker Jupyter Notebooks
`amazon-nova-samples/` and `AWS-GenAI-Contact-Center/whisper/` contain notebooks:
- Run in SageMaker Studio or local Jupyter
- Deploy models to SageMaker endpoints
- Use `boto3` Bedrock clients for inference

## Common AWS Patterns

### Bedrock Client Setup
```python
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
bedrock_agent = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
```

### Invoke Claude/Nova Models
```python
response = bedrock.invoke_model(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    body=json.dumps({'messages': [...], 'max_tokens': 1024})
)
```

### S3 Operations
```python
s3 = boto3.resource('s3')
s3.Bucket(bucket_name).upload_file(local_path, s3_key)
```

## Common Dependencies

**Python (Streamlit apps):**
- `streamlit`, `boto3`, `botocore`, `python-dotenv`, `pandas`, `Pillow`
- Claude SDK: `@anthropic-ai/bedrock-sdk` (Node.js)

**Node.js (Lambda):**
- `serverless`, `@aws-sdk/client-*` services
- `@anthropic-ai/bedrock-sdk`: `^0.9.1`

## Development Workflow

1. **Check prerequisites** in project `README.md` for AWS account requirements
2. **Configure AWS credentials** via `aws configure` or environment variables
3. **Install dependencies** per project type
4. **Run locally** or deploy according to project-specific instructions
5. Each project handles its own infrastructure (CloudFormation resources via Serverless or manual setup)

## Security

- Never commit AWS credentials or `.env` files with secrets
- Use IAM roles with minimal required permissions per project
- Report security issues via AWS vulnerability reporting (do not create public issues)