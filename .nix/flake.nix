{
  description = "AI-Stock development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = pkgs.python314.withPackages (ps: with ps; [
          uv
          # add whatever GUI.py / stock_analysis.py actually need,
          # e.g. yfinance isn't in nixpkgs — install via pip in a venv if needed
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.python314Packages.pip
          ];

          shellHook = ''
            echo "AI-Stock dev shell (python $(python --version))"
          '';
        };
      });
}
