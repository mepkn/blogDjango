import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig((mode) => {
  return {
    plugins: [],
    base: "/static/",
    build: {
      manifest: true,
      emptyOutDir: true,
      outDir: resolve("./dist"),
      rollupOptions: {
        input: {
          tailwind: resolve("./src/style.css"),
        },
      },
    },
  };
});
