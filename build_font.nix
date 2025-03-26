{ pkgs ? import <nixpkgs> {}, version, transliteration }:

pkgs.stdenv.mkDerivation rec {
	pname = "${transliteration}-fonts";
	inherit version;
	name = "${pname}-${version}";

	src = pkgs.lib.cleanSource ./.;

	sourceFonts = pkgs.fetchFromGitHub {
		owner = "dejavu-fonts";
		repo = "dejavu-fonts";
		rev = "version_2_37";
		sha256 = "sha256-c5EJ9IlT5lPMVPZsBhyOi1B21xi5WLHJ6O0gAcWjdvY=";
	};

	nativeBuildInputs = [
		pkgs.fontforge
		pkgs.python3
	];

	buildPhase = ''
		mkdir ./out
		./build.sh -o out -t ./transliterations/${transliteration}.tsv $(find ${sourceFonts}/src/ -type f -name '*.sfd' -not -name '*MathTeXGyre.sfd')
	'';

	installPhase = ''
		find ./out/ \( -name '*.otf' -o -name '*.ttf' -o -name '*.woff' -o -name '*.woff2' \) -exec install -m444 -Dt $out/share/fonts/truetype {} \;
		install -m444 -Dt $out/share/doc/${name} ./readme.md

		for i in "AUTHORS" "NEWS" "LICENSE"; do
			install -m444 -Dt $out/share/doc/${name} ${sourceFonts}/$i
		done
	'';

	meta = with pkgs.lib; {
		description = "Transliteration fonts based on DejaVu Fonts";
		license = pkgs.lib.licenses.ofl;
	};
}
