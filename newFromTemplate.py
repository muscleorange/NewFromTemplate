import os, codecs,time, sublime, sublime_plugin

PLUGIN_NAME = 'NewFromTemplate'
SYNTAX_KEY = 'syntax'
DEFAULT_SYNTAX_FILE = 'Packages/HTML/HTML.tmLanguage'

class NewFromTemplateCommand(sublime_plugin.TextCommand):
	def run(self, edit, ext):
		view = sublime.active_window().new_file()
		template = get_template_file(ext)
		view.insert(edit, 0, rend_template(template))
		view.set_syntax_file(get_syntax_file(ext))
		if ext == 'java':
			view.set_name("example.java");

def get_settings():
	settings = sublime.load_settings(PLUGIN_NAME + '.sublime-settings')
	return settings


#get syntax file
def get_syntax_file(ext):
	settings = get_settings()
	if settings.get(SYNTAX_KEY) is None:
		return DEFAULT_SYNTAX_FILE
	syntaxs = settings.get(SYNTAX_KEY)
	if ext in syntaxs:
		return syntaxs.get(ext)
	return DEFAULT_SYNTAX_FILE

#get template directory path
def get_templates_path():
	packages_path = sublime.packages_path()
	return os.path.join(packages_path,PLUGIN_NAME,'templates')

#read template file
def get_template_file(ext):
	template_dir = get_templates_path()
	file_path = os.path.join(template_dir,ext+'.tmpl')
	if os.path.exists(file_path):
		return read_file(file_path)
	return ''

#read a file
def read_file(path):
	return codecs.open(path,"r","utf-8").read()

#rend a template file, replace variables with values
def rend_template(tmpl_str):
	settings = get_settings()
	author = settings.get('author')
	for atrr in author:
		tmpl_str = tmpl_str.replace('$%s$' % atrr, author.get(atrr))
	date_format = settings.get('date_format', '%d/%m/%Y')
	tmpl_str = tmpl_str.replace('$date$', time.strftime(date_format))
	encoding = settings.get('encoding', 'UTF-8')
	return tmpl_str.replace('$encoding$', encoding)