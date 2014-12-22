import os
import jinja2
import fns

from webapp2_extras import i18n

########################################################################
#Definiciones de Jinja2 para los templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), extensions=['jinja2.ext.i18n'], autoescape=True)
jinja_env.install_gettext_translations(i18n)
jinja_env.filters['first_date'] = fns.first_date
jinja_env.filters['datetimeformat'] = fns.datetimeformat
jinja_env.filters['datetimeformatchat'] = fns.datetimeformatchat

# jinja2 config with i18n enabled
config = {'webapp2_extras.jinja2': {'template_path': 'templates', 'environment_args': {'extensions': ['jinja2.ext.i18n']}}}
AVAILABLE_LOCALES = ['es_ES', 'en_US']


def render_str(template, **params):
    j = jinja_env.get_template(template)
    return j.render(params)
