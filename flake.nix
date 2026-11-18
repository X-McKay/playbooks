{
  description = "Reproducible Playbooks development environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      supportedSystems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              git
              just
              nixfmt
              python312
              shellcheck
              uv
            ];

            env = {
              UV_PYTHON = "${pkgs.python312}/bin/python";
              UV_PYTHON_DOWNLOADS = "never";
            };

            shellHook = ''
              echo "Playbooks development shell"
              echo "Run 'just bootstrap' once, then 'just check'."
            '';
          };
        }
      );

      checks = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python312.withPackages (
            ps: with ps; [
              jsonschema
              pyyaml
              rich
              rich-argparse
              markdown-it-py
            ]
          );
          source = pkgs.lib.cleanSourceWith {
            src = ./.;
            filter =
              path: type:
              !(builtins.elem (baseNameOf path) [
                ".git"
                ".venv"
                ".ruff_cache"
                "__pycache__"
                "artifacts"
                "dist"
              ]);
          };
        in
        {
          source-quality =
            pkgs.runCommand "playbooks-source-quality"
              {
                nativeBuildInputs = [
                  python
                  pkgs.ruff
                  pkgs.shellcheck
                  pkgs.nixfmt
                ];
              }
              ''
                cp -R ${source} source
                chmod -R u+w source
                cd source
                export PYTHONPATH="$PWD/tools/agentctl/src"
                nixfmt --check flake.nix
                shellcheck scripts/agentctl
                ruff check tools/agentctl/src tools/agentctl/tests scripts examples
                ruff format --check tools/agentctl/src tools/agentctl/tests scripts examples
                python scripts/check_docs.py
                python -m agentctl --no-animations skills validate skills
                touch "$out"
              '';
        }
      );

      formatter = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.nixfmt
      );
    };
}
