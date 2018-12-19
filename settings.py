class ResourcePaths(object):
    
    def __init__(self):
        pass

    @property
    def wp_jquery_path(self):
        return "http://kbase.us/wp-includes/js/jquery/jquery.js?ver=1.12.4"

    @property
    def wp_jquery_migrate_path(self):
        return "http://kbase.us/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1"
    
    @property
    def wp_theme_path(self):
        return "http://kbase.us/wp-content/themes/kbase-wordpress-theme/js/src/kbaseUtils.js?ver=4.7.3"
    
    @property
    def wp_json_path(self):
        return "http://kbase.us/wp-json/"
        
    @property
    def fontawsome_path(self):
        return "https://use.fontawesome.com/releases/v5.6.1/css/all.css"
    # TODO: what do I do with integrity??

    @property
    def lit_css_path(self):
        return "https://cdn.jsdelivr.net/npm/@ajusa/lit@latest/dist/lit.css"
    
    @property
    def bootstrap_css_path(self):
        return "//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css"
    
    @property
    def wp_grid_css_path(self):
        return "http://kbase.us/wp-content/themes/kbase-wordpress-theme/css/grid.css?ver=4.7.3"

    @property
    def wp_bootstrap_css_path(self):
        return "http://kbase.us/wp-content/themes/kbase-wordpress-theme/bootstrap/css/bootstrap.min.css?ver=4.7.3"
    
    @property
    def wp_bootstrap_theme_css_path(self):
        return "http://kbase.us/wp-content/themes/kbase-wordpress-theme/bootstrap/css/bootstrap-theme.css?ver=4.7.3"
