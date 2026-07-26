import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite runs the React app on http://localhost:5173
// FastAPI runs on http://localhost:8000
//
// The proxy below is how they connect in development:
// when the browser calls /api/..., Vite forwards that request to FastAPI.
// The browser only talks to :5173, so you avoid CORS headaches during local work.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
