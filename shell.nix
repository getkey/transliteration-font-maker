{ pkgs ? import <nixpkgs> {} }:

let
	liberation-fonts = pkgs.fetchFromGitHub {
		owner = "liberationfonts";
		repo = "liberation-fonts";
		rev = "49e1358e4017577429c9f8c39a3e6e879093264e";
		sha256 = "sha256-GCCl2sGfYZ56tLNbvBvyzMZJoJ8kbHFtLpkwNRBKll4=";
	};
in
pkgs.mkShell {
	buildInputs = [
		pkgs.fontforge-gtk
		pkgs.python3
	];

	shellHook = ''
		export LIBERATION_FONTS=${liberation-fonts}
	'';
}
