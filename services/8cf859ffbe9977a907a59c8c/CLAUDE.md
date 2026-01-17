# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django-Vue3-Admin is an enterprise-level admin system with two backend services and a Vue3 frontend:

- **backend/** - Django 5.2 + Django REST Framework, manages system resources (users, roles, menus, permissions)
- **ai_service/** - FastAPI service for AI/LLM functionality (chat, drawing, knowledge bases)
- **web/** - Vue3 vben-admin monorepo (Ant Design Vue)
- **docker/** - Docker Compose configurations for dev/prod deployment

## Development Commands

### Backend (Django)
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver  # http://localhost:8000

# Generate CRUD code (both backend + frontend)
python manage.py generate_crud <app_name> <ModelName> --frontend

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Import city/area data
python manage.py import_city_area_data
```

### AI Service (FastAPI)
```bash
cd ai_service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8010  # http://localhost:8010/docs
```

### Frontend (Vue3 vben-admin)
```bash
cd web
pnpm install
pnpm run dev:antd  # http://localhost:5678
```

### Docker Development
```bash
cd docker
cp .env.example .env.local  # Configure environment
docker compose -f ../docker-compose.dev.yml up -d --build
docker compose -f ../docker-compose.dev.yml down
```

## Architecture

### Backend Pattern: CustomModelViewSet

All API views inherit from `CustomModelViewSet` (utils/custom_model_viewSet.py) which provides:
- Standardized response format: `{"code": 0, "message": "ok", "data": {...}}`
- Action-based serializers via `action_serializers` dict
- Permission control via `action_permissions` dict
- Soft delete support via `enable_soft_delete` flag

```python
class MyViewSet(CustomModelViewSet):
    queryset = MyModel.objects.filter(is_deleted=False)
    serializer_class = MySerializer
    action_serializers = {
        'list': MyListSerializer,
        'create': MyCreateSerializer,
    }
```

### URL Structure (Backend)
- `api/admin/system/` - System management (users, roles, menus, depts, posts, configs)
- `api/admin/ai/` - AI features (models, conversations, messages, drawings, knowledge)
- `admin/` - Django Admin (disabled in DEMO_MODE)

### LLM Adapter Pattern

AI services use a factory pattern with interchangeable adapters:

| Provider | Adapter | Models |
|----------|---------|--------|
| DeepSeek | `llm/adapter/deepseek.py` | deepseek-chat |
| OpenAI | `llm/adapter/openai.py` | gpt-4, gpt-3.5-turbo |
| Tongyi | `llm/adapter/tongyi.py` | qwen-plus, wanx_v1 |
| Google | `llm/adapter/genai.py` | gemini-pro |

Factory: `llm/factory.py:get_adapter(provider, api_key, model, **kwargs)`

### Database Models

Core models inherit from `CoreModel` (utils/models.py) providing:
- `id`, `create_time`, `update_time`, `creator`, `modifier`, `is_deleted`, `remark`
- Status field with `CommonStatus` enum (abled/disabled)

Common status field: `status = SmallIntegerField(choices=CommonStatus.choices, default=CommonStatus.DISABLED)`

### AI Feature Models

- **ChatConversation** - Chat sessions with model config
- **ChatMessage** - Individual messages (user/assistant types)
- **ChatRole** - AI personas with system_message, knowledge, tools
- **AIModel** - LLM provider configurations
- **Knowledge** - RAG knowledge bases with embedding model
- **Drawing** - AI image generation tasks (Midjourney-style)

### Permissions System

Button-level permissions via `v-permission` directive in Vue. Backend validates using `HasButtonPermission` which checks `app:model:action` permission codes.

### Middleware

- **IdempotencyMiddleware** - Prevents duplicate form submissions
- **DemoModeMiddleware** - (DEMO_MODE=true) Blocks all POST/PUT/DELETE operations globally

### Celery Tasks

- Worker: `celery -A backend worker -l info`
- Beat scheduler: `celery -A backend beat -l info`
- Monitor: `celery -A backend flower --port=5555 --basic_auth=admin:admin123`

## Environment Variables

Key environment variables (docker/.env.*):
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` - MySQL connection
- `REDIS_HOST`, `REDIS_PORT` - Redis for caching/sessions/celery
- `DEMO_MODE` - Enable demo mode (read-only)
- `DEEPSEEK_API_KEY`, `DASHSCOPE_API_KEY` - LLM API keys

## Key Files

- `backend/backend/settings.py` - Django settings, middleware, celery config
- `backend/utils/custom_model_viewSet.py` - Base ViewSet with standard response wrapper
- `backend/ai/models.py` - AI feature models (conversations, messages, roles, knowledge)
- `ai_service/llm/factory.py` - LLM adapter factory
- `backend/system/management/commands/generate_crud.py` - CRUD code generator