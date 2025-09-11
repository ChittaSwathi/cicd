Links that i followed to do the setup:
https://www.capitalone.com/tech/software-engineering/demystifying-devops-getting-started-with-automated-delivery-pipelines/
https://dashboard.ngrok.com/get-started/setup/macos
https://ngrok.com/docs/integrations/github/webhooks/#start-your-app

# CI/CD with GitHub → Jenkins (local tunneling via ngrok)

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
```
your-repo/
├── Jenkinsfile
└── startup.sh
```

**`startup.sh`**
```bash
#!/bin/bash
# Simple script run by the pipeline
echo "Hello from Jenkins Pipeline!"
```

**`Jenkinsfile`**
```groovy
pipeline {
  agent any

  stages {
    stage('Prepare') {
      steps {
        sh 'chmod +x startup.sh'
      }
    }

    stage('Build') {
      steps {
        sh './startup.sh'
      }
    }

    stage('Deploy') {
      steps {
        echo 'Deploying application (mock step)...'
      }
    }
  }
}
```

Commit and push:
```bash
git init
git add .
git commit -m "Initial: Jenkinsfile + startup.sh"
git branch -M main
git remote add origin https://github.com/<you>/<your-repo>.git
git push -u origin main
```

---

### 2. Expose Jenkins with ngrok

Start ngrok:
```bash
ngrok http 8080
```

Copy the HTTPS URL, e.g.:
```
https://<id>.ngrok-free.app
```

Set Jenkins’ public URL:
- **Manage Jenkins → System → Jenkins Location → Jenkins URL**  
  `https://<id>.ngrok-free.app/`

Enable CSRF proxy compatibility:
- **Manage Jenkins → Configure Global Security → CSRF Protection → Enable proxy compatibility**

---

### 3. Configure the GitHub webhook

In GitHub repo → **Settings → Webhooks → Add webhook**:
- **Payload URL**: `https://<id>.ngrok-free.app/github-webhook/` (trailing slash required ✅)
- **Content type**: `application/json`
- **Secret**: leave blank (unless configured in Jenkins)
- **Events**: “Just the push event”

---

### 4. Create a Jenkins job

**Option A: Pipeline (Script from SCM)**
- New Item → *Pipeline*
- **Build Triggers**: ✅ GitHub hook trigger for GITScm polling
- **Pipeline Definition**: *Pipeline script from SCM*
  - SCM: Git
  - Repository URL: `https://github.com/<you>/<your-repo>.git`
  - Branches to build: `*/main`
  - Script Path: `Jenkinsfile`

**Option B: Multibranch Pipeline**
- New Item → *Multibranch Pipeline*
- Add GitHub/Git source → repo URL
- Build Configuration: Jenkinsfile
- Build Triggers: Build when a change is pushed to GitHub
- Run “Scan Repository Now”

---

### 5. Trigger a build with a push

Make a change and push:
```bash
echo "# CI test" >> README.md
git add README.md
git commit -m "Trigger build via webhook"
git push
```

A new Jenkins build should start automatically.

---

## 🛠️ Troubleshooting & Fixes

### Issue 1: 403 Invalid HTTP Response
- **Cause:** Wrong endpoint or CSRF block  
- **Fix:** Use `https://<ngrok>.ngrok-free.app/github-webhook/` (HTTPS + trailing slash), enable proxy compatibility, and align secrets.

### Issue 2: 302 Redirect
- **Cause:** Webhook URL missing trailing slash  
- **Fix:** Use `https://<ngrok>.ngrok-free.app/github-webhook/`

### Issue 3: 200 OK but no build
- **Cause:** Event was `ping`, not `push`  
- **Fix:** Commit & push code to the correct branch

### Issue 4: Branch mismatch
- **Cause:** Job set to `*/main` but pushed to `master/feature`  
- **Fix:** Adjust Branch Specifier (e.g. `*/main` or `**`)

### Issue 5: Repo mismatch
- **Cause:** Jenkins job SCM URL doesn’t match pushed repo  
- **Fix:** Ensure Repository URL matches your remote (`git remote -v`)

### Issue 6: CSRF / crumb errors
- **Cause:** Origin/Referer blocked by Jenkins  
- **Fix:** Enable proxy compatibility, ensure Jenkins URL = ngrok URL

### Issue 7: ngrok URL changes
- **Cause:** ngrok restarted, new URL  
- **Fix:** Update Jenkins URL + GitHub webhook Payload URL

### Issue 8: Manual build works, webhook says “No changes”
- **Cause:** Jenkins saw no new commits on branch  
- **Fix:** Ensure commit pushed to same branch & repo as configured

---

## ✅ Quick Checklist

- [ ] Jenkins URL = `https://<ngrok>.ngrok-free.app/`  
- [ ] GitHub webhook = `https://<ngrok>.ngrok-free.app/github-webhook/` (trailing slash)  
- [ ] Content type = `application/json`  
- [ ] Secret blank in both, or identical in both  
- [ ] Build trigger enabled (GitHub hook trigger for GITScm polling)  
- [ ] Repo URL matches, credentials valid  
- [ ] Branch Specifier matches your branch (`*/main` or `**`)  
- [ ] Pushed a real commit (not just webhook ping)  

---

## 📓 Summary

With this setup:
- Any commit pushed to `main` triggers Jenkins via GitHub webhook  
- Jenkins runs the pipeline defined in `Jenkinsfile`  
- ngrok provides a temporary public URL for GitHub to reach your local Jenkins  

This is the simplest working demo of **GitHub → Jenkins CI/CD** on a local machine.
