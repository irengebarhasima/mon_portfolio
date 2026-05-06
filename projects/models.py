from django.db import models
from django.contrib.contenttypes.fields import GenericRelation  # ← à ajouter
from core.models import Comment, Like  , Rating# ← à ajouter

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relations inverses génériques (permettent d'utiliser project.comments.all())
    comments = GenericRelation(Comment, related_query_name='project')
    likes = GenericRelation(Like, related_query_name='project')
    ratings = GenericRelation(Rating, related_query_name='project')  #

    # Méthodes de comptage
    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()
        # ==================================================
    # MÉTHODE POUR LA NOTE MOYENNE
    # ==================================================
    def average_rating(self):
        """Calcule la note moyenne du projet (arrondie à 0.5 près)"""
        ratings = self.ratings.all()
        if ratings:
            avg = sum(r.value for r in ratings) / ratings.count()
            # Arrondir à 0.5 près (ex: 4.2 → 4.5, 4.6 → 5.0)
            return round(avg * 2) / 2
        return 0  # Pas encore de notes
    
    def total_ratings(self):
        """Nombre total d'évaluations"""
        return self.ratings.count()

    def __str__(self):
        return self.title
        

