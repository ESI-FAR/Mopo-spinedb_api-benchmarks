{
  description = "Run spinedb_api";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      this-py = pkgs.python312;
      py-deps = ps: with ps; [
        #livereload
      ];
      deps = with pkgs; [
        fontconfig
        freetype
        kcachegrind
        libxkbcommon
        pipenv
        postgresql
        py-spy
        sqlite
        xorg.libX11
        xorg.libX11.dev

        (this-py.withPackages py-deps)
      ];
    in {
      devShells.default = pkgs.mkShell {
        packages = deps;

      # Environment variables
      # fixes libstdc++ issues and libgl.so issues
      #LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/:${pkgs.glib.out}/lib/:${pkgs.qt6.full.out}/lib/:${pkgs.fontconfig.lib}/lib/";
      LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath deps}:${pkgs.stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/:${pkgs.glib.out}/lib/:${pkgs.qt6.full.out}/lib/:${pkgs.fontconfig.lib}/lib/";
      #LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib/:${pkgs.glib.out}/lib/";

      # fixes xcb issues :
      QT_PLUGIN_PATH="${pkgs.qt6.qtbase}/${pkgs.qt6.qtbase.qtPluginPrefix}";
      };
    });
}
