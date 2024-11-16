from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ImageCreateForm


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
