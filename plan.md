# Dockerfile Improvement Plan

## 1. Introduction

This document outlines a plan to improve the existing `Dockerfile` to make it more secure, efficient, and production-ready.

## 2. Current State

The current `Dockerfile` is well-structured and follows some best practices, but there are several areas where it can be improved.

## 3. Areas for Improvement

*   **Dependencies Not Using Lock Files:** The current `Dockerfile` installs dependencies from `pyproject.toml`, which does not guarantee reproducible builds.
*   **Missing Security Hardening:** The current `Dockerfile` runs the application as the `root` user, which is a security risk.
*   **Test Running in Build:** The current `Dockerfile` runs tests in the same image as the application, which increases the image size.
*   **Health Check Could Be More Robust:** The current health check is very basic and could be improved to provide a more accurate indication of the application's health.
*   **No Multi-stage build:** The current `Dockerfile` does not use a multi-stage build, which results in a larger image size.
*   **No non-root user:** The current `Dockerfile` does not create a non-root user to run the application.
*   **Vague `COPY` instructions:** The current `Dockerfile` copies entire directories, which can be inefficient.
*   **Multiple `RUN` instructions:** The current `Dockerfile` has multiple `RUN` instructions, which can be combined to reduce the number of layers in the image.
*   **Incomplete `.dockerignore` file:** The `.dockerignore` file can be improved to exclude more project-specific files.

## 4. Recommendations

*   **Use Lock Files:** Update the `Dockerfile` to use `requirements.txt` and `requirements-dev.txt` for reproducible builds.
*   **Security:** Add a non-root user to the `Dockerfile` and run the application as that user.
*   **Multi-stage:** Use a multi-stage build to create a smaller production image.
*   **Production vs Dev:** Create separate `Dockerfile`s or use build arguments to create different images for production and development.
*   **Volume Mounts:** Use volumes for the `data/input` and `data/output` directories to persist data.
*   **Combine `RUN` instructions:** Combine `RUN` instructions to reduce the number of layers in the image.
*   **Update the `.dockerignore` file:** Update the `.dockerignore` file to exclude additional unnecessary files and directories from the build context.

## 5. Proposed `Dockerfile`

```dockerfile
# build stage
FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends git

COPY pyproject.toml README.md ./
COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY src/ ./src/
COPY tests/ ./tests/

RUN python -m pytest tests/ -v

# production stage
FROM python:3.10-slim as production

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system app && adduser --system --group app

COPY --from=builder /app/src ./src
COPY --from=builder /app/pyproject.toml .
COPY --from=builder /app/README.md .
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

USER app

CMD ["python", "src/main.py"]

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import src.main; print('OK')" || exit 1
```

## 6. Next Steps

1.  Update the `.dockerignore` file.
2.  Replace the existing `Dockerfile` with the proposed `Dockerfile`.
3.  Build the new Docker image using the command: `docker build -t my-app .`
4.  Run the new Docker container using the command: `docker run -p 5000:5000 my-app`
