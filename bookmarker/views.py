from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings

import redis

from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action

# connect to Redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is submitted
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            data = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image added successfully')
            # redirect to new created image detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        'bookmarker/image/create.html',
        {'section': 'images', 'form': form},
    )


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr(f'image:{image.id}:views')

    # increment image ranking by 1
    r.zincrby('image_ranking', 1, image.id)
    return render(request, 'bookmarker/image/detail.html',
                  {'image': image, 'total_views': total_views})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)

            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page_number = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            'bookmarker/image/list_images.html',
            {'section': 'images', 'images': images},
        )
    return render(
        request,
        'bookmarker/image/list.html',
        {'section': 'images', 'images': images},
    )


@login_required
def image_ranking(request):
    # get the image ranking dictionary from redis
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

    return render(request, 'bookmarker/image/ranking.html',
                  {'section': 'images', 'most_viewed': most_viewed})
