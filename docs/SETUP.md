# Setup Guide

## Prerequisites

- Node.js 18+ and npm
- Python 3.12+
- PostgreSQL database (local or cloud)

## Database Setup

### Option 1: Local PostgreSQL

1. Install PostgreSQL on your machine
2. Create a database:
```bash
createdb trading_platform
```

3. Run the schema:
```bash
psql -d trading_platform -f database/schema.sql
```

### Option 2: Supabase (Recommended for Development)

1. Create a free account at https://supabase.com
2. Create a new project
3. Go to SQL Editor and run the contents of `database/schema.sql`
4. Get your database connection string from Settings > Database

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file:
```bash
cp .env.example .env
```

6. Edit `.env` with your configuration:
```
DATABASE_URL=postgresql://user:password@localhost/trading_platform
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

7. Run the server:
```bash
python app.py
```

Backend will run on http://localhost:5000

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

4. Run the development server:
```bash
npm run dev
```

Frontend will run on http://localhost:3000

## Verification

1. Test backend health:
```bash
curl http://localhost:5000/api/health
```

2. Test frontend:
Open http://localhost:3000 in your browser

## Troubleshooting

### Backend Issues

**ImportError: No module named 'psycopg2'**
- Install binary version: `pip install psycopg2-binary`

**Database connection error**
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify database exists

### Frontend Issues

**Module not found errors**
- Run `npm install` in frontend directory

**TypeScript errors**
- These are normal during development
- Will resolve after `npm install`

**Tailwind CSS not working**
- Ensure postcss.config.js exists
- Run `npm install` again

## Next Steps

After setup:
1. Test API endpoints using Postman or curl
2. Create a test user via `/api/auth/register`
3. Login via `/api/auth/login` to get token
4. Use token to access protected endpoints
