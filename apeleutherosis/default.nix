{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation rec {
	pname = "apeleutherosis-fonts";
	version = "0.0.0-2.1.5";

	src = pkgs.lib.cleanSource ./..;

	liberation = pkgs.fetchFromGitHub {
		owner = "liberationfonts";
		repo = "liberation-fonts";
		rev = version;
		sha256 = "Wg1uoD2k/69Wn6XU+7wHqf2KO/bt4y7pwgmG7+IUh4Q=";
	};

	nativeBuildInputs = [
		pkgs.fontforge
		pkgs.python3
	];

	buildPhase = ''
		cd ./apeleutherosis/
		mkdir ./out
		./build.sh -o out ${liberation}/src/*.sfd
	'';

	installPhase = ''
		find ./out/ \( -name '*.otf' -o -name '*.ttf' -o -name '*.woff' -o -name '*.woff2' \) -exec install -m444 -Dt $out/share/fonts/truetype {} \;
		install -m444 -Dt $out/share/doc/${pname}-${version} ./readme.md

		for i in "AUTHORS" "ChangeLog" "LICENSE"; do
			install -m444 -Dt $out/share/doc/${pname}-${version} ${liberation}/$i
		done
	'';

	meta = with pkgs.lib; {
		description = "Apeleutherosis Fonts, transliterations for latin and greek based on Liberation Fonts";
		license = pkgs.lib.licenses.ofl;
	};
}
