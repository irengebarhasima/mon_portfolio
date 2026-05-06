# core/views_comment.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from projects.models import Project
import json

@csrf_exempt
def add_comment_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            model_name = data.get('model')
            object_id = data.get('object_id')
            author_name = data.get('author_name')
            author_email = data.get('author_email')
            content = data.get('content')

            if not all([model_name, object_id, author_name, author_email, content]):
                return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)

            if model_name == 'project':
                try:
                    obj = Project.objects.get(id=object_id)
                except Project.DoesNotExist:
                    return JsonResponse({'error': 'Projet non trouvé'}, status=404)
                ct = ContentType.objects.get_for_model(Project)
            else:
                return JsonResponse({'error': 'Modèle non supporté'}, status=400)

            comment = Comment.objects.create(
                author_name=author_name,
                author_email=author_email,
                content=content,
                content_type=ct,
                object_id=object_id
            )

            return JsonResponse({
                'success': True,
                'id': comment.id,
                'author_name': comment.author_name,
                'content': comment.content,
                'created_at': comment.created_at.strftime("%d/%m/%Y %H:%M"),
                'total_comments': Comment.objects.filter(content_type=ct, object_id=object_id).count()
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)