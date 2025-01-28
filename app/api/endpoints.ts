const BASE_URL = process.env.NODE_ENV === 'development'
? 'http://localhost:8000/api/py'
: `http://${process.env.VERCEL_URL}/api/py`;

export const ENDPOINTS = {
  softStories: `${BASE_URL}/soft-stories`,
  tsunami: `${BASE_URL}/tsunami-zones`,
  liquefaction: `${BASE_URL}/liquefaction-zones`,
};