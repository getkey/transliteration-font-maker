{ pkgs ? import <nixpkgs> {} }:
	pkgs.mkShell {
		buildInputs = [
			pkgs.fontforge-gtk
			pkgs.python3
			pkgs.font-manager
		];
}
