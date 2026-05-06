
from django.shortcuts import render, get_object_or_404
from .models import Project

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q  # ← importe uniquement Q
from django.db import models

def project_list(request):
    """Affiche tous les projets avec recherche et pagination"""
    query = request.GET.get('q', '')
    
    if query:
        all_projects = Project.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(technologies__icontains=query)
        ).order_by('-created_at')
    else:
        all_projects = Project.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(all_projects, 6)
    page = request.GET.get('page', 1)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    return render(request, 'projects/list.html', {
        'projects': projects,
        'query': query
    })
# ==================================================
# VUE POUR LE DÉTAIL D'UN PROJET
# ==================================================
# Cette vue affiche un seul projet avec ses détails,
# ses commentaires, ses likes et son système de notation.
# ==================================================

def project_detail(request, project_id):
    """Affiche les détails complets d'un projet"""
    project = get_object_or_404(Project, id=project_id)
    
    # Calculer le nombre d'étoiles pleines pour l'affichage
    avg_rating = project.average_rating()
    full_stars = int(avg_rating)  # Nombre d'étoiles pleines
    half_star = (avg_rating - full_stars) >= 0.5  # Demi-étoile ? (pour 0.5)
    
    context = {
        'project': project,
        'avg_rating': avg_rating,
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(5 - full_stars - (1 if half_star else 0)),
    }
    return render(request, 'projects/detail.html', context)