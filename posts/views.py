# Defaults
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
# Created
from posts.models import Post, Category
from posts.forms import PostForm


# Global variable to be usable with multi view functions
categories = Category.objects.all()


def home_page(request, category=None):
    """ Mutual view for all posts and search results."""
    title = 'Home page'
    posts = Post.objects.all()

    # Filter by category
    if category:
        posts = Post.objects.filter(categories__name__icontains=category)

    # Search results
    query = request.GET.get('query')
    if query and not query.isspace():
        # Change page title
        title = 'Search results'
        # Get related query posts
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Pagination
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        # First page
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # Last page
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


def details_post(request, id):
    post = get_object_or_404(Post, id=id)

    context = {
        'title': 'Post',
        'post': post,
        'categories': categories,
    }

    return render(request, 'post-details.html', context)


def create_post(request):
    form = PostForm(request.POST or None)

    context = {
        'title': 'Create Post',
        'form': form,
    }

    return render(request, 'create-post.html', context)
