# Food Recipe Cloud-Native Application

This repository contains the full source code and deployment configuration for a cloud-native food recipe web application. The app includes:

- A **React frontend**
- An **Express backend** with MongoDB
- **Kubernetes manifests** for deployment
- **Locust test scripts** for performance/load testing
- A **Google Cloud Function (Serverless)** for sending email notifications

---

## 📁 Repository Structure

```
backend/                 # Express backend source code
frontend/                # React frontend source code
k8s/                     # Kubernetes deployment and service manifests
locust-tests/            # Locust load testing scripts
sendEmailFunction/       # Google Cloud Function for email
README.md                # Project overview and setup instructions
```

---

## ✅ Prerequisites

- Node.js (v16 or higher)
- Docker
- Kubernetes & kubectl (e.g., minikube or GKE)
- MongoDB (on VM in google cloud)
- Google Cloud CLI (`gcloud`)
- Locust (for performance testing)
---

## 🧑‍💻 Local Development Setup

### Backend (Express + MongoDB)

```bash
cd backend
npm install
npm run dev
```

Ensure your `.env` file includes:

```env
PORT=5000
MONGO_URI=your-mongodb-uri
JWT_SECRET=your-secret
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

- Frontend runs on: http://<frontend_external_ip>  
- Backend runs on: http://<backend_external_ip>:5000

external ips can be seen by "kubectl get svc" command after deployment

---

## 🚀 Kubernetes Deployment (Minikube or GKE)

Apply all deployment and service manifests:

```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

Check pod and service status:

```bash
kubectl get pods
kubectl get svc
```


---

## ☁️ Serverless Email Notification (Google Cloud Function)

Deploy the function from `sendEmailFunction/` directory:

```bash
gcloud functions deploy sendEmail \
  --runtime=nodejs18 \
  --trigger-http \
  --entry-point=sendEmail \
  --allow-unauthenticated \
  --set-env-vars=EMAIL_USER=<your_email>,EMAIL_PASS=<your_app_password>
```

---

## 📈 Load Testing with Locust

Start Locust with the provided script:

```bash
cd locust-tests
locust -f locustfile.py
```

Then visit [http://localhost:8089](http://localhost:8089) and start testing your backend endpoints.

---


## 🔐 Environment Configuration

Make sure both frontend and backend have access to the correct `.env` configuration in local or production setups. Backend expects:

- `PORT`
- `MONGO_URI`
- `JWT_SECRET`
