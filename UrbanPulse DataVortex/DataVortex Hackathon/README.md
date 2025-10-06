# UrbanPulse AI – Smart Emergency Traffic Management System

“Empowering cities to clear the path for life-saving vehicles — intelligently and instantly.”

## Stack
- Backend: FastAPI (Python 3.11), YOLOv8n, Supabase, OpenTelemetry → OTLP HTTP
- Frontend: Next.js 14, TailwindCSS, Framer Motion, Supabase Auth
- DB: Supabase (detections, traffic_signals, routes, users)

## Setup
1. Supabase: create project, set tables with `supabase/schema.sql`.
2. Configure env:
   - Backend: create `backend/.env` from `.env.example` and set `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE`, `OTLP_ENDPOINT`.
   - Frontend: create `frontend/.env.local` with `NEXT_PUBLIC_BACKEND_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`.

## Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Endpoints:
- POST `/detect/frame` (file=frame) → YOLOv8 detections, spans: preprocess/inference/postprocess/db.insert/schedule_signals
- POST `/simulate/gps_point` → store/update route, predict next points
- POST `/signal/update`, GET `/signal/all`
- GET `/stats/summary`

## Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000`.

## Tracing
- Default OTLP: `http://localhost:4318/v1/traces`
- Responses include `x-trace-id` for correlation.

## Deployment
- Backend: Render/Railway (Dockerfile included)
- Frontend: Vercel
- Supabase: cloud-managed
