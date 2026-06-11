FROM nginx:alpine

COPY index.html styles.css Restaurante.jpeg app.js /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]

