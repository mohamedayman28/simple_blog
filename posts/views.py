
from posts.models import Post, Category
from posts.forms import PostForm, CommentForm

# Defaults
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404


# Global variable to be usable within multi view functions
categories = Category.objects.all()


def home_page(request, category=None):
    """ Mutual view for all posts and search results."""

    title = 'Home page'
    posts = Post.objects.all()

    # Filter by category.
    if category:
        posts = Post.objects.filter(categories__name__icontains=category)

    # Search results.
    query = request.GET.get('query')
    if query and not query.isspace():
        # Change page title.
        title = 'Search results'
        # Get related query posts.
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Pagination.
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # Last page.
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'posts': paginated_queryset,
        'categories': categories,
        #   If posts are related to search query. Paginate the search results
        # using the query as a string parameter
        'query': query
    }

    return render(request, 'home.html', context)


def post_details(request, id):
    """ Show post details and handle the comment form."""

    try:
        post = Post.objects.get(id=id)

        # Handle Comment form.
        if request.method == 'POST':
            form = CommentForm(request.POST)
            # Populate form instance.
            form.instance.commenter = request.user
            form.instance.post = post
            form.instance.content = request.POST.get('content')

            if form.is_valid():
                form.save()
                messages.success(request, 'Thanks for your comment!!.')
                return redirect(reverse('posts:details', kwargs={'id': post.id}))

    except (Post.DoesNotExist, ValueError):
        messages.warning(request, 'Post does not exist.')
        return redirect('posts:home_page')

    context = {
        'categories': categories,
        'post': post,
    }

    return render(request, 'post-details.html', context)


@login_required(login_url="accounts:signin")
def post_form(request, id=None):
    """ Create/Update/Delete operations in one view."""
    context = {
        'categories': categories,
        'title': None,
        'form': None,
        'post': None,
    }

    try:
        author = request.user.author

        # If user is an author
        if author:
            # Post model CRUD operations.
            # Delete request.
            if request.resolver_match.url_name == 'delete':
                post = get_object_or_404(Post, id=id)
                messages.success(request, f'{post.title} deleted.')
                post.delete()
                return redirect('posts:home_page')
            # NOTE: Both Update and Create request related to the same HTML.
            # Update request with model instance for the form.
            elif request.resolver_match.url_name == 'update':
                context['title'] = 'Update post'
                post = get_object_or_404(Post, id=id)
                form = PostForm(request.POST or None, instance=post)
                # Next to general render.
            # Create request with regular form.
            elif request.resolver_match.url_name == 'create':
                context['title'] = 'Create new post'
                form = PostForm(request.POST or None)
                # Next to general render.

            # Form actions associated with Update and Create requests.
            if request.method == 'POST':
                if form.is_valid():
                    form.instance.author = author
                    form.save()
                    messages.success(request, f'{form.instance.title} Created')
                    return redirect(
                        reverse('posts:details', kwargs={
                                'id': form.instance.id})
                    )

            # General render. Mutual between Create and Update.
            context['form'] = form
            return render(request, 'create-post.html', context)

    # If user is not an author.
    except Exception as e:
        messages.warning(request, e)
        return redirect('posts:home_page')
