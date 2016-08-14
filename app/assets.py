import os
from flask_assets import Bundle

join = os.path.join
css_assets = Bundle('css/yeti.css',
                    'css/main.css',
                    'css/overrides.css',
                    'css/treeview.css',
                    filters='cssmin',
                    output='packed/packed.css'
                    )

js_assets = Bundle(
                   'js/jquery.min.js',
                   'js/jquery.cookie.js',
                   'js/bootstrap.js',
                   'js/main.js',
                   'js/treeview.js',
                #    join('js', 'jquery-3.1.0.min.js'),
                   filters='rjsmin',
                   output='packed/packed.js'
                   )


css_chm = Bundle(join('styles', 'Presentation.css'),
                 output=join('packed/chm_packed.css')
                 )

js_chm = Bundle('scripts/EventUtilities.js',
                'scripts/SplitScreen.js',
                'scripts/Dropdown.js',
                'scripts/script_manifold.js',
                'scripts/script_feedBack.js',
                'scripts/CheckboxMenu.js',
                'scripts/CommonUtilities.js',
                filters='rjsmin',
                output=join('packed/chm_packed.jss')
                )
