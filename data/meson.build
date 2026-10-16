gnome.compile_resources(
  meson.project_name(),
  'com.github.ANewJanuary.WikeSauce.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir
)

desktop_file = i18n.merge_file(
  input: 'com.github.ANewJanuary.WikeSauce.desktop.in',
  output: 'com.github.ANewJanuary.WikeSauce.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'com.github.ANewJanuary.WikeSauce.metainfo.xml.in',
  output: 'com.github.ANewJanuary.WikeSauce.metainfo.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'metainfo')
)

appstreamcli = find_program('appstreamcli', required: false)
if appstreamcli.found()
  test('Validate appstream file',
    appstreamcli,
    args: ['validate', '--no-net', '--explain', appstream_file],
    workdir: meson.current_build_dir()
  )
endif

install_data('com.github.ANewJanuary.WikeSauce.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

install_data(
  'com.github.ANewJanuary.WikeSauce.SearchProvider.ini',
  install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'gnome-shell', 'search-providers')
)

configure_file(
  input: 'com.github.ANewJanuary.WikeSauce.SearchProvider.service.in',
  output: 'com.github.ANewJanuary.WikeSauce.SearchProvider.service',
  configuration: conf,
  install: true,
  install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'dbus-1', 'services')
)

configure_file(
  input: 'com.github.ANewJanuary.WikeSauce.service.in',
  output: 'com.github.ANewJanuary.WikeSauce.service',
  configuration: conf,
  install: true,
  install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'dbus-1', 'services')
)

icondir = join_paths(get_option('prefix'), get_option('datadir'), 'icons', 'hicolor')
install_data('icons/com.github.ANewJanuary.WikeSauce.svg', install_dir: join_paths(icondir, 'scalable/apps'))
install_data('icons/com.github.ANewJanuary.WikeSauce-symbolic.svg', install_dir: join_paths(icondir, 'symbolic/apps'))
