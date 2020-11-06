from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


def explore(request):
    peoples_fetch_qs = apps.get_model('star_wars_test', 'PeopleFetch').objects.all().order_by('-fetching_date')
    context = {"collections": peoples_fetch_qs}
    return render(request, 'explore.html', context)


def collection_download(request, collection_id):
    from django.http import FileResponse
    PeopleFetch = apps.get_model('star_wars_test', 'PeopleFetch')
    people_fetch = get_object_or_404(PeopleFetch, id=collection_id)
    path_to_file = people_fetch.file_path
    return FileResponse(open(path_to_file, 'rb'))


def collection(request, collection_id):
    PeopleFetch = apps.get_model('star_wars_test', 'PeopleFetch')
    people_fetch = get_object_or_404(PeopleFetch, id=collection_id)
    # TODO: create a form to validate the get param limit is a well formatted integer
    limit = int(request.GET.get("limit", 10))
    next_limit = limit + 10
    html_table = people_fetch.get_html_etl_table(limit=limit)
    context = {
        "collection": people_fetch,
        "next_limit": next_limit,
        "html_table": html_table,
    }
    return render(request, 'collection.html', context)


def fetch(request):
    apps.get_model('star_wars_test', 'PeopleFetch').objects.fetch()
    return HttpResponseRedirect("/")
