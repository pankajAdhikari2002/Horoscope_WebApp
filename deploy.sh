#!/bin/bash

# Exit on error
set -e

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pip python3-venv nginx

# Create application directory
sudo mkdir -p /var/www/horoscope
sudo chown www-data:www-data /var/www/horoscope

# Copy application files
sudo cp -r ./* /var/www/horoscope/
sudo cp .env /var/www/horoscope/

# Create and activate virtual environment
cd /var/www/horoscope
sudo python3 -m venv venv
sudo chown -R www-data:www-data venv
source venv/bin/activate

# Install dependencies
sudo -u www-data venv/bin/pip install -r requirements.txt

# Setup systemd service
sudo cp horoscope.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start horoscope
sudo systemctl enable horoscope

# Setup Nginx
sudo cp horoscope.nginx /etc/nginx/sites-available/horoscope
sudo ln -sf /etc/nginx/sites-available/horoscope /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo "Deployment complete! Your application should be running now."
