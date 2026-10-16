configure_file(
  input: 'wikesauce.in',
  output: 'wikesauce',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'wikesauce-sp.in',
  output: 'wikesauce-sp',
  configuration: conf,
  install: true,
  install_dir: pkgdatadir
)

wike_sources = [
  '__init__.py',
  'application.py',
  'bookmarks.py',
  'customtheme.py',
  'data.py',
  'history.py',
  'langlinks.py',
  'languages.py',
  'menu.py',
  'page.py',
  'prefs.py',
  'search.py',
  'toc.py',
  'view.py',
  'wikipedia.py',
  'window.py'
]

install_data(wike_sources, install_dir: moduledir)
