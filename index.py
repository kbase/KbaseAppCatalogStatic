from flask import Flask, url_for, request, render_template
import os
import requests
import json
from collections import defaultdict
from werkzeug.wsgi import DispatcherMiddleware

app = Flask(__name__)

app.config['APPLICATION_ROOT'] = os.environ.get('ROOT_PREFIX', '/applist')
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    app.config['APPLICATION_ROOT']: app
})


_kbase_url = os.environ.get('KBASE_ENDPOINT', 'https://ci.kbase.us/services')

if _kbase_url is None:
    raise RuntimeError('Missing host address')

_catalog_url = _kbase_url + '/catalog'
# Narrative Method Store URL requre rpc at the end. 
# ref L43/44 https://github.com/kbase/narrative_method_store/blob/master/scripts/nms-listmethods.pl 
_NarrativeMethodStore_url = _kbase_url + '/narrative_method_store/rpc'


# drop down menu options 
options = ['Organize by', 'All apps', 'Category', 'Module', 'Developer']

# Ref: https://github.com/kbase/kbase-ui-plugin-catalog/blob/master/src/plugin/modules/data/categories.yml
# Category ID/Category name map
Category_names = {
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
    'uncategorized' : 'Uncategorized Apps'
}
# categorires in order
category_order = ['Read Processing', 'Genome Assembly', 'Genome Annotation', 'Sequence Analysis', 'Comparative Genomics', 'Metabolic Modeling', 'Expression', 'Microbial Communities', 'Utilities', 'Uncategorized Apps']


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
    organized_app_list = defaultdict(lambda: [])
    if organize_by == "All apps":
        for app in app_list:
            # If the organized by item does not exisit in app information, then add to All Apps list.
            organized_app_list['All apps'].append(app)
    else:
        for app in app_list:    
            if len(app.get(organize_by, [])) > 0:
                # list of categories/developers/modules associated with the app.
                items = app.get(organize_by)
                # Modules are not in an array. Any option that are no in an array and a string, store in an array to avoid string iteration.
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
                        'git_commit_hash' : git_commit_hash,
                        'include_compilation_report': 1
                    }]
    }
    
    module_resp = requests.post(_catalog_url, data=json.dumps(module_payload))
    try:
        module_resp_json = module_resp.json()
        # App info is stored in the first element of the result array.

    except ValueError as err:
        print(err)
    
    git_repo_url = module_resp_json['result'][0]['git_url'] + '/tree/' + git_commit_hash + '/ui/narrative/methods/' + app_name
    
    return git_repo_url

# payload for using NarrativeMethodStore to get all apps.
payload = {
    'id': 0,
    'method': 'NarrativeMethodStore.list_methods',
    'version': '1.1',
    'params': [{"tag":"release"}]
}

@app.route('/', methods=['GET'])
def get_apps():
    resp = requests.post(_NarrativeMethodStore_url, data=json.dumps(payload))
    try:
        resp_json = resp.json()
        # Apps are stored in the first element of the result array.
        app_list = resp_json['result'][0]

    except:
        return render_template('error.html')
    
    # remove apps with "inactive" or "viewers" or "importers" in categories.
    clean_app_list = remove_inactive(app_list)

    # Get value from dropdown menue from url parameter
    option = request.args.get('organize_by')
    
    # Initialize organized app list.  organized_list is passed to index.html template. 
    organized_list ={}

    if option == None or option == "Category":
        # When the page loads and drop down menue has not been used, return category-sorted.
        sorted_list = sort_app('categories', clean_app_list)
        
        # Get correct name for each category.
        app_list_name = {}

        for category in sorted_list:
            if (category != 'active') and (category != 'upload'):
                cat_name = Category_names.get(category)
                app_list_name[cat_name] = sorted_list.get(category)

        # Sort list by the order in category_order list.
        for item in category_order:
            organized_list[item] = app_list_name.get(item)
        
    elif option == "All apps":
        organized_list = sort_app("All apps", clean_app_list)

    elif option == "Module":
        organized_list = sort_app('module_name', clean_app_list)

    elif option == "Developer":
        organized_list = sort_app('authors', clean_app_list)

    else:
        print("this shouldn't happen!")
    
    return render_template('index.html', options=options, organized_list=organized_list )

@app.route('/')
def index():
    return 'index'

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
    response = requests.post(_NarrativeMethodStore_url, data=json.dumps(app_page_payload))
    try:
        response_json = response.json()
        # App info is stored in the first element of the result array.
        app_info = response_json['result'][0][0]

    except:
        return render_template('error.html')

    git_url = get_git_url(app_module, app_name, app_info['git_commit_hash'])

    return render_template('app_page.html', app=app_info, git_url=git_url)