#!/bin/bash

# Mise à jour de pip
pip install --upgrade pip

# Installation des dépendances
pip install -r requirements.txt

# Collecte des fichiers statiques
python manage.py collectstatic --noinput

# Application des migrations
python manage.py migrate

# Création du superutilisateur automatiquement (si non existant)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell