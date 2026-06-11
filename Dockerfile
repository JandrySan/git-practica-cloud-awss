FROM nginx:alpine

# Copia tu nginx.conf que está en la raíz
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia tus archivos estáticos de la raíz al directorio de Nginx
COPY index.html /usr/share/nginx/html/
COPY app /usr/share/nginx/html/app.js
COPY styles /usr/share/nginx/html/styles.css

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]