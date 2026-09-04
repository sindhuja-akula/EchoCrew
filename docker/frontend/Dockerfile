FROM nginx:alpine

# Copy static frontend web application files
COPY frontend /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
