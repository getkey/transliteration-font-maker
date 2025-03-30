{ pkgs ? import <nixpkgs> {} }:
	pkgs.mkShell {
		buildInputs = [
			pkgs.python3
			pkgs.python3Packages.fonttools
			pkgs.python3Packages.sortedcontainers
		];
}
