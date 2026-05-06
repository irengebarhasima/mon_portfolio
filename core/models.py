from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ContentBlock(models.Model):
    """
    Bloc de contenu modifiable depuis l'admin.
    key : identifiant unique (ex: 'home_title', 'about_text', 'skills')
    content : texte (peut contenir du HTML)
    """
    key = models.CharField(max_length=100, unique=True)
    content = models.TextField(help_text="Vous pouvez utiliser du HTML simple (balises <br>, <strong>, etc.)")

    def __str__(self):
        return self.key


class Like(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'session_key')

class Comment(models.Model):
    # Contenu
    author_name = models.CharField(max_length=100, verbose_name="Votre nom")
    author_email = models.EmailField(verbose_name="Votre email (non affiché)")
    content = models.TextField(verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True)

    # Lien générique vers n'importe quel objet (projet, service...)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']  # du plus récent au plus ancien

    def __str__(self):
        return f"Commentaire de {self.author_name} sur {self.content_object}"
        
# ==================================================
# MODÈLE D'ÉVALUATION (NOTES)
# ==================================================
# Ce modèle permet aux visiteurs de noter un projet de 1 à 5 étoiles.
# Chaque visiteur ne peut noter qu'une seule fois par projet (via session_key)
# ==================================================

class Rating(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)  # Identifiant unique du visiteur
    value = models.IntegerField(choices=[(1, '1★'), (2, '2★'), (3, '3★'), (4, '4★'), (5, '5★')])  # Note de 1 à 5
    
    # Liaison générique avec n'importe quel modèle (Project, Service, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('content_type', 'object_id', 'session_key')  # Empêche un même visiteur de voter plusieurs fois
    
    def __str__(self):
        return f"Note {self.value}★ pour {self.content_object}"