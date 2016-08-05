import os
from flask_assets import Bundle

join = os.path.join
css_assets = Bundle(join('css', 'bootstrap.css'),
                    join('css', 'main.css'),
                    join('css', 'overrides.css'),
                    filters='cssmin',
                    output='packed/packed.css'
                    )

js_assets = Bundle(join('js', 'jquery-3.1.0.min.js'),
                   join('js', 'bootstrap.js'),
                   join('js', 'main.js'),
                   filters='rjsmin',
                   output='packed/packed.js'
                   )


css_chm = Bundle(join('styles', 'Presentation.css'),
                 output=join('packed/chm_packed.css')
                 )

js_chm = Bundle(join('scripts', 'EventUtilities.js'),
                join('scripts', 'SplitScreen.js'),
                join('scripts', 'Dropdown.js'),
                join('scripts', 'script_manifold.js'),
                join('scripts', 'script_feedBack.js'),
                join('scripts', 'CheckboxMenu.js'),
                join('scripts', 'CommonUtilities.js'),
                filters='rjsmin',
                output=join('packed/chm_packed.jss')
                )
