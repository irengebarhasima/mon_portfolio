from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from .models import Like
from projects.models import Project
import json

@csrf_exempt
def toggle_like(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            model_name = data.get('model')
            object_id = int(data.get('object_id'))
            
            if model_name == 'project':
                model = Project
            else:
                return JsonResponse({'error': 'Modèle non supporté'}, status=400)
            
            # Récupérer la session
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            
            content_type = ContentType.objects.get_for_model(model)
            
            # Chercher ou créer le like
            like, created = Like.objects.get_or_create(
                content_type=content_type,
                object_id=object_id,
                session_key=session_key
            )
            
            if not created:
                # Si le like existe déjà, on le supprime (unlike)
                like.delete()
                liked = False
            else:
                liked = True
            
            # Compter les likes pour cet objet
            like_count = Like.objects.filter(
                content_type=content_type,
                object_id=object_id
            ).count()
            
            return JsonResponse({
                'liked': liked,
                'count': like_count,
                'success': True
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e), 'success': False}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)