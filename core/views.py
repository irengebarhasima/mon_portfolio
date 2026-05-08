
from django.shortcuts import render
from projects.models import Project
from services.models import Service
from .models import ContentBlock
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404
from .models import Like
from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from projects.models import Project
from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Rating
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json



def home(request):
    projects = Project.objects.all().order_by('-created_at')[:3]
    services = Service.objects.all()[:4]
    
    # Récupération des blocs de texte
    home_title = ContentBlock.objects.get(key='home_title').content
    home_slogan = ContentBlock.objects.get(key='home_slogan').content
    
    context = {
        'projects': projects,
        'services': services,
        'home_title': home_title,
        'home_slogan': home_slogan,
    }
    return render(request, 'core/home.html', context)
def about(request):
    about_text = ContentBlock.objects.get(key='about_text').content
    skills = ContentBlock.objects.get(key='skills').content
    return render(request, 'core/about.html', {
        'about_text': about_text,
        'skills': skills,
    })
    

def add_comment_simple(request, model_name, object_id):
    if request.method == 'POST':
        if model_name == 'project':
            project = get_object_or_404(Project, id=object_id)
            content_type = ContentType.objects.get_for_model(Project)
            
            Comment.objects.create(
                author_name=request.POST.get('author_name'),
                author_email=request.POST.get('author_email'),
                content=request.POST.get('content'),
                content_type=content_type,
                object_id=object_id
            )
    return redirect('project_list')
    


def toggle_like_simple(request, project_id):
    """Version simple du like avec rechargement de page"""
    project = get_object_or_404(Project, id=project_id)
    content_type = ContentType.objects.get_for_model(Project)
    
    # Gestion de la session
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    # Chercher ou créer le like
    like, created = Like.objects.get_or_create(
        content_type=content_type,
        object_id=project_id,
        session_key=session_key
    )
    
    if not created:
        # Si le like existe déjà, on le supprime
        like.delete()
    
    # Rediriger vers la même page
    return redirect(request.META.get('HTTP_REFERER', 'project_list'))
    
    
    
# Ajoutez ces imports en haut de core/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from projects.models import Project

# Ajoutez cette fonction à la fin de core/views.py
@require_POST
@csrf_exempt
def api_toggle_like(request):
    """API AJAX pour gérer les likes"""
    try:
        data = json.loads(request.body)
        model_name = data.get('model')
        object_id = data.get('object_id')
        
        if model_name == 'project':
            obj = get_object_or_404(Project, id=object_id)
            content_type = ContentType.objects.get_for_model(Project)
        else:
            return JsonResponse({'error': 'Modèle non supporté'}, status=400)
        
        # Gestion de la session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        # Chercher ou créer le like
        like, created = Like.objects.get_or_create(
            content_type=content_type,
            object_id=object_id,
            session_key=session_key
        )
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        # Compter les likes
        like_count = Like.objects.filter(
            content_type=content_type,
            object_id=object_id
        ).count()
        
        return JsonResponse({
            'liked': liked,
            'count': like_count
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
        
# ==================================================
# VUE POUR GÉRER LES NOTES (ÉVALUATIONS)
# ==================================================
# Cette vue permet à un visiteur de noter un projet.
# Elle utilise la session pour empêcher un même visiteur
# de voter plusieurs fois.
# ==================================================



def rate_project(request, project_id):
    """Gère l'ajout ou la modification d'une note pour un projet"""
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        
        # Vérifier que la note est entre 1 et 5
        if 1 <= rating_value <= 5:
            project = get_object_or_404(Project, id=project_id)
            content_type = ContentType.objects.get_for_model(Project)
            
            # Gestion de la session
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            
            # Chercher si l'utilisateur a déjà noté ce projet
            existing_rating = Rating.objects.filter(
                content_type=content_type,
                object_id=project_id,
                session_key=session_key
            ).first()
            
            if existing_rating:
                # Mettre à jour la note existante
                existing_rating.value = rating_value
                existing_rating.save()
            else:
                # Créer une nouvelle note
                Rating.objects.create(
                    session_key=session_key,
                    value=rating_value,
                    content_type=content_type,
                    object_id=project_id
                )
    
    # Rediriger vers la page de détail du projet
    return redirect('project_detail', project_id=project_id)