#!/bin/bash
set -e

sudo apt update
sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx git
sudo systemctl enable docker
sudo systemctl start docker

if [ ! -d "TPchet" ]; then git clone <your-tpchet-repo>.git; fi
cd TPchet

if [ ! -f "backend/.env" ]; then
cat <<EOL > backend/.env
DATABASE_URL=postgresql://postgres:postgres@db:5432/tpchet
SECRET_KEY=tpchet_secret
STRIPE_SECRET_KEY=sk_live_yourkey
STRIPE_WEBHOOK_SECRET=whsec_yourkey
EOL
fi

docker-compose up -d --build

NGINX_CONF="/etc/nginx/sites-available/tpchet.conf"
sudo tee $NGINX_CONF > /dev/null <<EOL
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    location / { proxy_pass http://localhost:3000; proxy_http_version 1.1; proxy_set_header Upgrade \$http_upgrade; proxy_set_header Connection 'upgrade'; proxy_set_header Host \$host; proxy_cache_bypass \$http_upgrade; }
    location /api/ { proxy_pass http://localhost:8000/; proxy_set_header Host \$host; proxy_set_header X-Real-IP \$remote_addr; }
    location /webhook/ { proxy_pass http://localhost:8000/webhook/; proxy_set_header Host \$host; proxy_set_header X-Real-IP \$remote_addr; }
}
EOL
sudo ln -sf /etc/nginx/sites-available/tpchet.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -
