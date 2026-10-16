# Build WikeSauce with Nix: nix-build
# Based on the nixpkgs package for Wike.

{ pkgs ? import <nixpkgs> { } }:

pkgs.python3Packages.buildPythonApplication {
  pname = "wikesauce";
  version = "3.2.1";
  pyproject = false; # built with meson

  src = pkgs.lib.cleanSource ./.;

  nativeBuildInputs = with pkgs; [
    meson
    pkg-config
    ninja
    appstream
    desktop-file-utils
    gobject-introspection
    wrapGAppsHook4
  ];

  buildInputs = with pkgs; [
    glib
    gtk4
    librsvg
    libadwaita
    glib-networking
    webkitgtk_6_0
  ];

  dependencies = with pkgs.python3Packages; [
    requests
    pygobject3
  ];

  # prevent double wrapping
  dontWrapGApps = true;
  preFixup = ''
    makeWrapperArgs+=("''${gappsWrapperArgs[@]}")
  '';
  postFixup = ''
    wrapPythonProgramsIn "$out/share/wikesauce" "$out ''${pythonPath[*]}"
  '';

  meta = {
    description = "Wikipedia reader for the GNOME Desktop, with custom themes";
    homepage = "https://github.com/ANewJanuary/Wike";
    license = pkgs.lib.licenses.gpl3Plus;
    platforms = pkgs.lib.platforms.linux;
    mainProgram = "wikesauce";
  };
}
