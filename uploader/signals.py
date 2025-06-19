from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import ComicInteraction, ClassicComic, ModernComic, models

@receiver([post_save, post_delete], sender=ComicInteraction)
def update_comic_metrics(sender, instance, **kwargs):
    if instance.classic_comic:
        comic = instance.classic_comic
        metrics = ComicInteraction.objects.filter(classic_comic=comic).aggregate(
            avg_rating=Avg('rating'), view_count=Count('id', filter=models.Q(viewed=True))
        )
        comic.average_rating = metrics['avg_rating'] or 0.0
        comic.view_count = metrics['view_count'] or 0
        comic.save()
    elif instance.modern_comic:
        comic = instance.modern_comic
        metrics = ComicInteraction.objects.filter(modern_comic=comic).aggregate(
            avg_rating=Avg('rating'), view_count=Count('id', filter=models.Q(viewed=True))
        )
        comic.average_rating = metrics['avg_rating'] or 0.0
        comic.view_count = metrics['view_count'] or 0
        comic.save()