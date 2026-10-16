# This file is part of Wike (com.github.hugolabe.Wike)
# SPDX-FileCopyrightText: 2021-25 Hugo Olabera
# SPDX-License-Identifier: GPL-3.0-or-later


from gi.repository import GLib, Gio, Gdk, Gtk, Adw

from wike.data import settings


# Optional colors for custom theme and default values for light and dark base

COLORS = (('background', _('Background')),
          ('foreground', _('Text')),
          ('accent', _('Accent')),
          ('link', _('Links')),
          ('sidebar', _('Sidebar')),
          ('surface', _('Infoboxes and Cards')))

DEFAULT_COLORS = ({ 'background': '#ffffff', 'foreground': '#1e1e1e', 'accent': '#3584e4',
                    'link': '#1c71d8', 'sidebar': '#ebebed', 'surface': '#f6f6f6' },
                  { 'background': '#222226', 'foreground': '#ffffff', 'accent': '#78aeed',
                    'link': '#99c1f1', 'sidebar': '#2e2e32', 'surface': '#2e2e32' })


# Get custom theme colors from settings (only valid colors)

def get_colors():
  colors = {}
  for key, value in settings.get_value('custom-colors').unpack().items():
    rgba = Gdk.RGBA()
    if rgba.parse(value):
      colors[key] = rgba.to_string()
  return colors


# Build css with libadwaita variables for app widgets

def custom_app_css():
  colors = get_colors()
  background = colors.get('background')
  foreground = colors.get('foreground')
  accent = colors.get('accent')
  sidebar = colors.get('sidebar')
  surface = colors.get('surface')
  rules = []

  if background:
    if not sidebar:
      shade = foreground or ('white' if settings.get_int('custom-base') == 1 else 'black')
      sidebar = 'color-mix(in srgb, ' + background + ' 92%, ' + shade + ')'
    for var in ('window-bg-color', 'headerbar-bg-color', 'dialog-bg-color', 'popover-bg-color'):
      rules.append('--' + var + ': ' + background + ';')
  if sidebar:
    for var in ('headerbar-backdrop-color', 'sidebar-bg-color', 'sidebar-backdrop-color', 'secondary-sidebar-bg-color', 'secondary-sidebar-backdrop-color', 'overview-bg-color'):
      rules.append('--' + var + ': ' + sidebar + ';')
  if surface or background:
    for var in ('view-bg-color', 'card-bg-color'):
      rules.append('--' + var + ': ' + (surface or background) + ';')
  if foreground:
    for var in ('window-fg-color', 'view-fg-color', 'headerbar-fg-color', 'sidebar-fg-color', 'secondary-sidebar-fg-color', 'card-fg-color', 'dialog-fg-color', 'popover-fg-color', 'overview-fg-color'):
      rules.append('--' + var + ': ' + foreground + ';')
  if accent:
    rules.append('--accent-bg-color: ' + accent + ';')
    rules.append('--accent-color: ' + accent + ';')

  css = ':root {' + ''.join(rules) + '}'
  if background:
    css += '.wikiview-status {background-color: ' + background + ';}'
  return css


# Build css for Wikipedia article view

def custom_view_css():
  colors = get_colors()
  background = colors.get('background')
  foreground = colors.get('foreground')
  link = colors.get('link') or colors.get('accent')
  surface = colors.get('surface')
  root_vars = ''
  css = ''

  if background:
    root_vars += '--background-color-base:' + background + '!important;'
    css += '#mw-mf-page-center,.mw-body{background-color:' + background + '!important}'
  if foreground:
    root_vars += '--color-base:' + foreground + '!important;--color-emphasized:' + foreground + '!important;'
    css += '.mw-body{color:' + foreground + '!important}'
  if link:
    root_vars += '--color-progressive:' + link + '!important;'
    css += '.mw-body a:not(.new){color:' + link + '!important}'
  if surface:
    root_vars += '--background-color-neutral-subtle:' + surface + '!important;'
    css += '.infobox,.infobox_v2,.infobox_v3,.gallerybox .thumb,.flexquote{background-color:' + surface + '!important}'
  if background or surface:
    css += '.wikitable{background:transparent!important}'

  if root_vars:
    css = 'html{' + root_vars + '}' + css
  return css


# Dialog to set custom theme base style and colors

@Gtk.Template(resource_path='/com/github/ANewJanuary/WikeSauce/gtk/custom-theme.ui')
class CustomThemeDialog(Adw.PreferencesDialog):

  __gtype_name__ = 'CustomThemeDialog'

  base_combo = Gtk.Template.Child()
  colors_group = Gtk.Template.Child()

  # Bind base style and add a row for each color

  def __init__(self):
    super().__init__()

    settings.bind('custom-base', self.base_combo, 'selected', Gio.SettingsBindFlags.DEFAULT)

    self._rows = {}
    colors = get_colors()
    for key, title in COLORS:
      switch = Gtk.Switch(valign=Gtk.Align.CENTER, active=key in colors)
      button = Gtk.ColorDialogButton(dialog=Gtk.ColorDialog(with_alpha=False), valign=Gtk.Align.CENTER, sensitive=key in colors)
      button.set_rgba(self._parse(colors.get(key, self._default_color(key))))

      row = Adw.ActionRow(title=title, activatable_widget=switch)
      row.add_prefix(switch)
      row.add_suffix(button)
      self.colors_group.add(row)
      self._rows[key] = (switch, button)

      switch.connect('notify::active', self._switch_active_cb, key)
      button.connect('notify::rgba', self._button_rgba_cb)

    handler_base = settings.connect('changed::custom-base', self._settings_base_changed_cb)
    self.connect('closed', lambda dialog: settings.disconnect(handler_base))

  # Parse color string to rgba

  def _parse(self, value):
    rgba = Gdk.RGBA()
    rgba.parse(value)
    return rgba

  # Get default color for current base style

  def _default_color(self, key):
    return DEFAULT_COLORS[settings.get_int('custom-base')][key]

  # Save enabled colors to settings

  def _save_colors(self):
    colors = {}
    for key, (switch, button) in self._rows.items():
      if switch.get_active():
        colors[key] = button.get_rgba().to_string()
    settings.set_value('custom-colors', GLib.Variant('a{ss}', colors))

  # On switch toggled enable color and save

  def _switch_active_cb(self, switch, param, key):
    button = self._rows[key][1]
    button.set_sensitive(switch.get_active())
    if not switch.get_active():
      button.set_rgba(self._parse(self._default_color(key)))
    self._save_colors()

  # On color changed save

  def _button_rgba_cb(self, button, param):
    if button.get_sensitive():
      self._save_colors()

  # On base style changed show default colors for disabled rows

  def _settings_base_changed_cb(self, settings, key):
    for color_key, (switch, button) in self._rows.items():
      if not switch.get_active():
        button.set_rgba(self._parse(self._default_color(color_key)))
