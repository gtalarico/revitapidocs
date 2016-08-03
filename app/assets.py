import os
from flask_assets import Bundle

join = os.path.join
css_assets = Bundle(join('css', 'bootstrap.css'),
                    join('css', 'main.css'),
                    join('css', 'overrides.css'),
                    filters='cssmin',
                    output='packed/packed.css'
                    )

js_assets = Bundle(join('js', 'bootstrap.js'),
                   join('js', 'main.js'),
                   filters='rjsmin',
                   output='packed/packed.js'
                   )


css_chm = Bundle(join('styles', 'presentation.css'),
                 output=join('packed_chm', 'packed.css')
                 )

js_chm = Bundle(join('scripts', 'EventUtilities.js'),
                join('scripts', 'SplitScreen.js'),
                join('scripts', 'Dropdown.js'),
                join('scripts', 'script_manifold.js'),
                join('scripts', 'script_feedBack.js'),
                join('scripts', 'CheckboxMenu.js'),
                join('scripts', 'CommonUtilities.js'),
                filters='rjsmin',
                output=join('packed_chm','packed.js')
                )
