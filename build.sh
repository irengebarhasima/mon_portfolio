#!/bin/bash

# Supprimez ou commentez les lignes pip install ici
# (C'est Render qui s'en charge maintenant avec la nouvelle Build Command)

# Application des migrations Django
python manage.py migrate
python manage.py migrate admin_interface
python manage.py collectstatic --noinput

# Création des blocs de contenu par défaut (si non existants)
echo "from core.models import ContentBlock; ContentBlock.objects.get_or_create(key='home_title', defaults={'content': 'Daniel Irenge Barhasima – Ingénieur en Réseaux & Télécoms'}); ContentBlock.objects.get_or_create(key='home_slogan', defaults={'content': 'Des données à la décision – solutions web, IoT et réseaux'}); ContentBlock.objects.get_or_create(key='about_text', defaults={'content': 'Ingénieur en Réseaux et Télécommunications avec une solide formation...'}); ContentBlock.objects.get_or_create(key='skills', defaults={'content': '<ul><li>Python, JavaScript, Java</li><li>Django, Node.js</li></ul>'}); ContentBlock.objects.get_or_create(key='contact_email', defaults={'content': 'irengebarhasima@gmail.com'}); ContentBlock.objects.get_or_create(key='contact_phone', defaults={'content': '+243 898 145 014'})" | python manage.py shell

# Création du superutilisateur admin (si non existant)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell
