const getBaseUrl = () => {
  if (typeof window !== "undefined") {
    // Running on the client
    return "";
  }

  if (process.env.VERCEL_ENV === "development") {
    return "http://localhost:8000/api";
  }

  if (process.env.VERCEL_ENV === "preview" || process.env.VERCEL_ENV === "production") {
    return `https://datasci-earthquake.vercel.app/api`;
  }

  return "http://localhost:8000/api"; // Fallback for local dev
};

const BASE_URL = getBaseUrl();

export const ENDPOINTS = {
  softStories: `${BASE_URL}/soft-stories`,
  tsunami: `${BASE_URL}/tsunami-zones`,
  liquefaction: `${BASE_URL}/liquefaction-zones`,
};