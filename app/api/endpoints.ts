const BASE_URL = process.env.NEXT_PUBLIC_API_URL ||
(process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}/api/py` : "http://localhost:8000/api/py");

export const ENDPOINTS = {
  softStories: `${BASE_URL}/soft-stories`,
  tsunami: `${BASE_URL}/tsunami-zones`,
  liquefaction: `${BASE_URL}/liquefaction-zones`,
};