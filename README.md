# CI/CD with GitHub → Jenkins (via ngrok)

This repo demonstrates a simple CI/CD pipeline where a **GitHub repo** triggers a **local Jenkins build** exposed through **ngrok**.

---

## 📦 Prerequisites

- Jenkins running locally (http://localhost:8080)
- Jenkins plugins:
  - Git plugin
  - GitHub plugin
  - (Optional) GitHub Branch Source (for Multibranch)
- GitHub account + repository
- [ngrok](https://ngrok.com/) installed and authenticated
- Git installed locally

---

## 🚀 Setup Instructions

### 1. Create the repo & add files

Repo structure:
