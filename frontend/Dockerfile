# Stage 1: build the static assets
FROM node:20-slim AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Vite bakes VITE_* env vars into the JS bundle at build time, so it must be
# passed as a build arg rather than a runtime environment variable.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Stage 2: serve the built files with a minimal static file server.
# Deliberately not using Nginx here to keep the stack to what's specified -
# `serve` is a lightweight, zero-config alternative for a static SPA.
FROM node:20-slim AS runtime

WORKDIR /app
RUN npm install -g serve@14

COPY --from=build /app/dist ./dist

EXPOSE 5173

# -s enables SPA fallback: unknown paths (e.g. a refresh on /links/3) serve
# index.html so React Router can handle the route client-side.
CMD ["serve", "-s", "dist", "-l", "5173"]
