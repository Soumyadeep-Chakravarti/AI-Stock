{
  description = "AI-Stock development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };

      in
      {
        devShells.default = pkgs.mkShellNoCC {
          packages = [
            pkgs.python314
            pkgs.uv
            pkgs.git
            pkgs.gh
            pkgs.just
            pkgs.pre-commit
            pkgs.ripgrep
            pkgs.fd
            pkgs.jq
            pkgs.yq-go
            pkgs.curl
            pkgs.httpie
            pkgs.sqlite
            pkgs.nixfmt
            pkgs.nil
            pkgs.statix
            pkgs.deadnix
            pkgs.shellcheck
            pkgs.shfmt
            pkgs.yamllint
            pkgs.actionlint
            pkgs.gitleaks
            pkgs.typos
            pkgs.pip-audit
          ];

          shellHook = ''
            export UV_PROJECT_ENVIRONMENT="$PWD/.venv"
          '';
        };
      }
    );
}
