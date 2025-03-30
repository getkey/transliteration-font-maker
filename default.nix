{ pkgs ? import <nixpkgs> {}, version }:

let
	pkgs = import <nixpkgs> {};
	buildFont = import ./build_font.nix;
	paramsList = [
		{
			transliteration = "iso_9_1995";
			sourceFont = "${pkgs.noto-fonts}/share/fonts/noto/NotoSans[wdth,wght].ttf";
		}
		{
			transliteration = "traditional_greek_romanization";
			sourceFont = "${pkgs.noto-fonts}/share/fonts/noto/NotoSans[wdth,wght].ttf";
		}
		{
			transliteration = "braille_romanization";
			sourceFont = "${pkgs.dejavu_fonts}/share/fonts/truetype/DejaVuSans.ttf";
		}
		{
			transliteration = "mkhedruli_romanization";
			sourceFont = "${pkgs.dejavu_fonts}/share/fonts/truetype/DejaVuSans.ttf";
		}
	];
	finalParamsList = builtins.map ({ transliteration, sourceFont }: { inherit transliteration; inherit sourceFont; version = version; }) paramsList;
	results = builtins.map buildFont finalParamsList;
in
results
