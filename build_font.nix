{ pkgs ? import <nixpkgs> {}, version, transliteration }:

pkgs.stdenv.mkDerivation rec {
	pname = "${transliteration}-fonts";
	inherit version;
	name = "${pname}-${version}";

	src = pkgs.lib.cleanSource ./.;

	nativeBuildInputs = [
		pkgs.python3
		pkgs.python3Packages.fonttools
		pkgs.python3Packages.sortedcontainers
		pkgs.noto-fonts
	];

	buildPhase = ''
		outname=$(echo ${transliteration} | tr '_' ' ' | awk '{ for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2); print }')
		mkdir -p "$out/share/fonts/${pname}"
		python3 ./swap.py -o "$out/share/fonts/${pname}/${transliteration}.ttf" -t './transliterations/${transliteration}.tsv' -n "$outname" '${pkgs.noto-fonts}/share/fonts/noto/NotoSans[wdth,wght].ttf'
	'';

	installPhase = ''
		install -m444 -Dt $out/share/doc/${pname} ./readme.md
	'';

	meta = with pkgs.lib; {
		description = "Transliteration fonts based on Noto Sans";
		license = pkgs.lib.licenses.ofl;
	};
}
