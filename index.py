from flask import Flask, url_for, request, render_template
import os
import requests
import json

app = Flask(__name__)

_kbase_url = os.environ.get('KBASE_ENDPOINT', 'https://ci.kbase.us/services')

# Narrative Method Store URL requre rpc at the end. 
# ref L43/44 https://github.com/kbase/narrative_method_store/blob/master/scripts/nms-listmethods.pl 
_NarrativeMethodStore_url = _kbase_url + '/narrative_method_store/rpc'
payload = {
    'id': 0,
    'method': 'NarrativeMethodStore.list_methods',
    'version': '1.1',
    'params': [{"tag":"release"}]
}

# drop down menu options 
options = ['Organize by', 'All apps', 'Category', 'Module', 'Developer']

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
    'Uncategorized' : 'Uncategorized Apps'
}


def has_inactive(categories):
  ''' Return False if an app has "inactive" or "viewers" or "importers" in categories.
    Args: A list of categories from an app. 
    Returns: False or nothing. '''
    for category in categories:
        if category == 'inactive' or category == "viewers" or category == "importers":
            break
        return False

def remove_inactive(app_list):
  ''' Remove apps with set categories from list of apps. 
       Args: A list of apps
       Returns: A new list of apps'''
    clean_app_list = []
    for app in app_list:
        if has_inactive(app['categories']) == False:
            clean_app_list.append(app)

    print(len(app_list), len(clean_app_list))
    return clean_app_list

def sort_app(organize_by, app_list):
''' Sort apps in 
    sort_app function takes in an array, organize_by, which is derived from drop down menu. 
        organize_by is an array of either categories, modules, or developers. 
        app_list is an array of all apps.
    It returns a dictionary of {key = category/developer/module : value = app }.
'''
    organized_app_list = {}
    for app in app_list:
        if app.get(organize_by) is not None:
            # check if it already exisits in the organized_app_list dictionary.
            items = app.get(organize_by)
            # Modules are not in an array. Any option that are no in an array and a string, store in an array to avoid string iteration.
            if isinstance(items, str):
                items = [items]

            for item in items:
                if item not in organized_app_list:
                    # if it is not alreay in the organized_app_list, then add category and the app associated. 
                    organized_app_list[item] = [app]
                elif item in organized_app_list:
                    # if category is already exisiting in the dictionay, then add the app to the list.
                    arr = organized_app_list.get(item)
                    arr.append(app)
                    organized_app_list[item] = arr
                else:
                    # This shouldn't happen.
                    pass
        else:
            # If the organized by item does not exisit in app information, then add to Uncategorized Apps list.
            if 'Uncategorized' not in organized_app_list:
                organized_app_list['Uncategorized'] = [app]
            elif 'Uncategorized' in organized_app_list:
                arr = organized_app_list.get('Uncategorized')
                arr.append(app)
                organized_app_list['Uncategorized'] = arr
            pass
    return organized_app_list

@app.route('/', methods=['GET'])
def get_apps():
    resp = requests.post(_NarrativeMethodStore_url, data=json.dumps(payload))
    try:
        resp_json = resp.json()
        # Apps are stored in the first element of the result array.
        app_list = resp_json['result'][0]
    except ValueError as err:
        #TODO: Find document on set ValueError
        print(err)
    
    # remove inactive apps.
    clean_app_list = remove_inactive(app_list)

    # get url for all authors
    
    # Get value from dropdown menue from url parameter
    option = request.args.get('organize_by')
    
    # Initialize organized app list.  organized_list is passed to index.html template. 
    organized_list ={}

    if option == None:
        # When the page loads and drop down menue has not been used, return all of the apps non-sorted.
        organized_list = {
            'All apps' : clean_app_list
        }

    elif option == "Category":
        sorted_list = sort_app('categories', clean_app_list)
        ''' line 798 https://github.com/kbase/kbase-ui-plugin-catalog/blob/master/src/plugin/modules/widgets/kbaseCatalogBrowser.js 
            line 82  self.categories = categoriesConfig.categories; 
            categoriesConfig <- yaml!../data/categories.yml 
            https://github.com/kbase/kbase-ui-plugin-catalog/blob/master/src/plugin/modules/data/categories.yml
            Line 330 line 363 https://github.com/kbase/narrative_method_store/blob/master/src/us/kbase/narrativemethodstore/NarrativeMethodStoreServer.java
            Line 588 https://github.com/kbase/narrative_method_store/blob/master/src/us/kbase/narrativemethodstore/db/github/LocalGitDB.java
            Line 316
            protected File getCategoriesDir() {
            return new File(gitLocalPath, "categories");
            }
            https://github.com/kbase/narrative_method_specs/tree/develop/categories
        also 
            https://github.com/kbase/kbase-ui-plugin-catalog/blob/master/src/plugin/modules/catalog_util.js
            line 81:
        this.skipApp = function(categories) {
            for(var i=0; i<categories.length; i++) {
                if(categories[i]=='inactive') {
                    return true;
                }
                if(categories[i]=='viewers') {
                    return true;
                }
                if(categories[i]=='importers') {
                    return true;
                }
            }
            return false;
        };

        '''
        # list_categories = requests.post(_NarrativeMethodStore_url, data=json.dumps({
        #                                                                                 'id': 0,
        #                                                                                 'method': 'NarrativeMethodStore.list_categories',
        #                                                                                 'version': '1.1',
        #                                                                                 'params': [{'load_methods': 0,
        #                                                                                 'load_apps': 0,
        #                                                                                 'load_types': 0,
        #                                                                                 'tag': 'release'}]
        #                                                                             }))
        # print(list_categories.json())
        # for category in sorted_list:
        #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', category)
        #     category_info = requests.post(_NarrativeMethodStore_url, data=json.dumps({
        #                                                                                 'id': 0,
        #                                                                                 'method': 'NarrativeMethodStore.get_category',
        #                                                                                 'version': '1.1',
        #                                                                                 'params': [{'ids': [category]}]
        #                                                                             }))
        #     print(category_info.json())

        #shape sorted_lisåt. need to get GetCategoryParams for each from narrative method store
        for category in sorted_list:
            # Skip Active and upload (it's not used??)
            if (category != 'active') and (category != 'upload'):
                cat_name = Category_names.get(category)
                # in Python, if dict size changes like below during iteration, it will throw up.          
                # sorted_list[cat_name] = sorted_list.pop(category).
                # Work around: making a new dict. 
                organized_list[cat_name] = sorted_list.get(category)
     
    elif option == "Module":
        organized_list = sort_app('module_name', clean_app_list)


    elif option == "Developer":
        #TODO: shape sorted_list. need to get developer names for each from ??
        organized_list = sort_app('authors', clean_app_list)

    else:
        print("this shouldn't happen!")
    
    return render_template('index.html', options=options, organized_list=organized_list )

