from flask_assets import Bundle

css_assets = Bundle('css/bootstrap.css',
                    'css/main.css',
                    'css/overrides.css',
                    filters='cssmin',
                    output='packed/packed.css')

js_assets = Bundle('js/bootstrap.js', 'js/main.js',
                   filters='rjsmin',
                   output='packed/packed.js')

css_chm = Bundle('styles/presentation.css',
                    output='packed_chm/packed.css')

js_chm = Bundle('scripts/EventUtilities.js',
                 'scripts/SplitScreen.js',
                 'scripts/Dropdown.js',
                 'scripts/script_manifold.js',
                 'scripts/script_feedBack.js',
                 'scripts/CheckboxMenu.js',
                 'scripts/CommonUtilities.js',
                  filters='rjsmin',
                  output='packed_chm/packed.js')
