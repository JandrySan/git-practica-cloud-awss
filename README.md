# Restaurante Familia Sanchez - Full Stack con CI/CD

Proyecto con frontend estatico en Google Cloud Run y backend FastAPI en AWS Elastic Beanstalk.

## URLs de produccion

- Frontend: https://git-practica-cloud-aws-194727093142.us-west1.run.app/
- Backend: http://restaurante-v2-env.eba-yimwd639.us-east-2.elasticbeanstalk.com/

## Como se conectan

El formulario del frontend envia las reservas a `/reserva` en el mismo dominio de Cloud Run.

Nginx recibe esa ruta en el contenedor del frontend y la reenvia al backend real:

```text
https://git-practica-cloud-aws-194727093142.us-west1.run.app/reserva
  -> http://restaurante-v2-env.eba-yimwd639.us-east-2.elasticbeanstalk.com/reserva
```

Esto evita problemas de CORS y mantiene el frontend apuntando siempre a su propio dominio.

## Secrets necesarios en GitHub Actions

Configura estos secrets en `Settings > Secrets and variables > Actions`:

| Secret | Uso |
| --- | --- |
| `AWS_ACCESS_KEY_ID` | Access key del usuario IAM para Elastic Beanstalk |
| `AWS_SECRET_ACCESS_KEY` | Secret key del usuario IAM para Elastic Beanstalk |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Provider completo de Workload Identity Federation |
| `GCP_SERVICE_ACCOUNT` | Cuenta de servicio de GCP usada por GitHub Actions |

## Despliegues

- Frontend: `.github/workflows/deploy-frontend.yml` construye la imagen con el `Dockerfile` de la raiz y despliega en Cloud Run.
- Backend: `.github/workflows/deploy-backend.yml` empaqueta `backend/` y despliega en Elastic Beanstalk.
- Cloud Build: `cloudbuild.yaml` hace el mismo build/deploy del frontend si se usa un trigger directo de Google Cloud Build.

## Endpoints del backend

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| GET | `/` | Informacion de la API |
| GET | `/health` | Health check |
| POST | `/reserva` | Crear una reserva |
| GET | `/reservas` | Listar reservas |

## Probar localmente

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend con Docker:

```bash
docker build -t restaurante-frontend .
docker run --rm -p 8080:8080 restaurante-frontend
```

Luego abre `http://localhost:8080`.
