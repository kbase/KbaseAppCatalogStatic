from flask import Flask, render_template
import os
import requests
import json
from collections import defaultdict
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

app.config['APPLICATION_ROOT'] = os.environ.get('ROOT_PREFIX', '/')

conf = dict()
conf['KBASE_ENDPOINT'] = os.environ.get('KBASE_ENDPOINT')
conf['DASHBOARD_ENDPOINT'] = os.environ.get('DASHBOARD_ENDPOINT')
conf['GA_TRACKING_ID'] = os.environ.get('GA_TRACKING_ID')
conf['AW_TRACKING_ID'] = os.environ.get('AW_TRACKING_ID')

assert os.environ.get('DASHBOARD_ENDPOINT', '').strip(), "DASHBOARD_ENDPOINT env var is required."
assert os.environ.get('KBASE_ENDPOINT', '').strip(), "KBASE_ENDPOINT env var is required."

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    app.config['APPLICATION_ROOT']: app
})

# Ref: https://github.com/kbase/kbase-ui-plugin-catalog/blob/master/src/plugin/modules/data/categories.yml
# Category ID/Category name map
_CATEGORY_NAMES = {
    'annotation': 'Genome Annotation',
    'assembly': 'Genome Assembly',
    'communities': 'Microbial Communities',
    'comparative_genomics': 'Comparative Genomics',
    'expression': 'Expression',
    'metabolic_modeling': 'Metabolic Modeling',
    'reads': 'Read Processing',
    'sequence': 'Sequence Analysis',
    'util': 'Utilities',
    'inactive': 'Inactive Methods',
    'viewers': 'Viewing Methods',
    'importers': 'Importing Methods',
    'featured_apps': 'Featured Apps',
    'active': 'Active Methods',
    'upload': 'Upload Methods',
    'uncategorized': 'Uncategorized Apps'
}
# categorires in order
_CATEGORY_ORDER = ['Read Processing', 'Genome Assembly', 'Genome Annotation',
                   'Sequence Analysis', 'Comparative Genomics', 'Metabolic Modeling',
                   'Expression', 'Microbial Communities', 'Utilities', 'Uncategorized Apps']


def has_inactive(categories):
    ''' Return True if an app has "inactive" or "viewers" or "importers" in categories.
    Args:
        categories: A list of categories from an app.
    Returns:
        Weather or not the app has "inactive" or "viewers" or "importers" in categories.
    '''

    if 'inactive' in categories or 'viewers' in categories or 'importers' in categories:
        return True
    return False


def remove_inactive(app_list):
    ''' Remove apps with certain categories ("inactive" or "viewers" or "importers") from list of apps.
    Args:
        app_list: A list of apps.
    Returns:
        A list of apps that do not in conatin categories.
    '''
    return [app for app in app_list if not has_inactive(app['categories'])]


def sort_app(organize_by, app_list):
    ''' Separate apps in chosen category/developer/module from the drop down menu.
    Args:
        organized_by: A string that is chosen by a user from the drop down menu.
        app_list: A list of apps.
    Returns:
        A dictionary of {key = category/developer/module : value = app }.
    '''
    organized_app_list = defaultdict(lambda: [])  # type: dict
    if organize_by == "All apps":
        for app in app_list:
            # If the organized by item does not exisit in app information, then add to All Apps list.
            organized_app_list['All apps'].append(app)
    else:
        for app in app_list:
            if len(app.get(organize_by, [])) > 0:
                # list of categories/developers/modules associated with the app.
                items = app.get(organize_by)
                # Modules are not in an array. Any option that are no in an array and a string, store in
                # an array to avoid string iteration.
                if isinstance(items, str):
                    items = [items]

                for item in items:
                    organized_app_list[item].append(app)
            else:
                # handling apps without Cat or Dev list.
                organized_app_list['uncategorized'].append(app)

    return organized_app_list


def get_git_url(module_name, app_name, git_commit_hash):
    ''' Return url of git repository of the app.
    Args:
        module_name: module name derived from app_id.
        app_name: app name derived from app_id.
        git_commit_hash: git commit hash of the app.
    Returns:
        Url of git repository.
    '''
    module_payload = {
        'id': 0,
        'method': 'Catalog.get_module_version',
        'version': '1.1',
        'params': [{
            'module_name': module_name,
            'git_commit_hash': git_commit_hash,
            'include_compilation_report': 1
        }]
    }

    module_resp = requests.post(conf['KBASE_ENDPOINT'] + '/catalog', data=json.dumps(module_payload))
    try:
        module_resp_json = module_resp.json()
        # App info is stored in the first element of the result array.

    except ValueError as err:
        print(err)

    git_url = module_resp_json['result'][0]['git_url']
    git_repo_url = git_url + '/tree/' + git_commit_hash + '/ui/narrative/methods/' + app_name

    return git_repo_url


# Narrative Method Store URL requre rpc at the end.
# ref L43/44 https://github.com/kbase/narrative_method_store/blob/master/scripts/nms-listmethods.pl
_NARRATIVE_METHOD_STORE_URL = conf['KBASE_ENDPOINT'] + '/narrative_method_store/rpc'

# payload for using NarrativeMethodStore to get all apps.
payload = {
    'id': 0,
    'method': 'NarrativeMethodStore.list_methods',
    'version': '1.1',
    'params': [{"tag": "release"}]
}


@app.route('/', methods=['GET'])
def get_apps():
    resp = requests.post(_NARRATIVE_METHOD_STORE_URL, data=json.dumps(payload))
    try:
        resp_json = resp.json()
        # Apps are stored in the first element of the result array.
        app_list = resp_json['result'][0]

    except Exception:
        return render_template('error.html')

    # remove apps with "inactive" or "viewers" or "importers" in categories.
    clean_app_list = remove_inactive(app_list)

    # Initialize organized app list.  organized_list is passed to index.html template.
    organized_list = {}

    # When the page loads and drop down menue has not been used, return category-sorted.
    sorted_list = sort_app('categories', clean_app_list)

    # Get correct name for each category.
    app_list_name = {}

    for category in sorted_list:
        if (category != 'active') and (category != 'upload'):
            cat_name = _CATEGORY_NAMES.get(category)
            app_list_name[cat_name] = sorted_list.get(category)

    # Sort list by the order in category_order list,
    # filter out the category that doesn't contain any apps,
    # save the number of categories for UI animation
    numCategories = 0
    for item in _CATEGORY_ORDER:
        if app_list_name.get(item):
            organized_list[item] = app_list_name.get(item)
            numCategories += 1

    # JSON format of Organized list.
    return render_template('index.html', conf=conf, organized_list=organized_list, numCategories=numCategories)


@app.route('/apps/<app_module>/<app_name>/<tag>', methods=['GET'])
@app.route('/apps/<app_module>/<app_name>', methods=['GET'])
def get_app(app_module, app_name, tag="release"):
    app_id = app_module + '/' + app_name

    app_page_payload = {
        'id': 0,
        'method': 'NarrativeMethodStore.get_method_full_info',
        'version': '1.1',
        'params': [{
            'ids': [app_id],
            'tag': tag
        }]
    }
    response = requests.post(_NARRATIVE_METHOD_STORE_URL, data=json.dumps(app_page_payload))
    try:
        response_json = response.json()
        # App info is stored in the first element of the result array.
        app_info = response_json['result'][0][0]

    except Exception:
        return render_template('error.html')

    git_url = get_git_url(app_module, app_name, app_info['git_commit_hash'])

    return render_template('app_page.html', conf=conf, app_id=app_id, app=app_info, git_url=git_url)
