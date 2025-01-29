export const fetchData = async (endpoint: string) => {
  try {
    console.log('Vercel URL:', process.env.VERCEL_URL);
    console.log("NEXT_PUBLIC_API_URL:", process.env.NEXT_PUBLIC_API_URL);
    console.log("BASE URL:", endpoint)
    const response = await fetch(endpoint, {
      cache: 'no-store',
    });
    if (!response.ok) {
      switch (response.status) {
        case 404:
          throw new Error("404 Not Found");
        case 500:
          throw new Error("500 Internal Server Error")
        default:
          throw new Error(response.status + " Unexpected Error")
      }
    }
    const data = await response.json();
    return data;
  } catch (error: any) {
    console.log("Error: " + error.message);
    return null;
  }
};
