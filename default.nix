{ pkgs ? import <nixpkgs> {}, version }:

let
	pkgs = import <nixpkgs> {};
	buildFont = import ./build_font.nix;
	hindSiliguri = pkgs.fetchFromGitHub {
		owner = "itfoundry";
		repo = "hind-siliguri";
		rev = "affb7dbd00dc554c33ecafc92cbfef5323ae5235";
		sha256 = "sha256-VgYZDiXPd0VskaLHJw8KnS3nlWbdGXf08nPvnNHBt6w";
	};
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
		{
			transliteration = "kunrei-shiki_hiragana_romanization";
			sourceFont = "${pkgs.ipafont}/share/fonts/opentype/ipag.ttf";
		}
		{
			transliteration = "iso_15919_bangla_romanization";
			sourceFont = "${hindSiliguri}/build/HindSiliguri-Regular.otf";
		}
	];
	finalParamsList = builtins.map ({ transliteration, sourceFont }: { inherit transliteration; inherit sourceFont; version = version; }) paramsList;
	results = builtins.map buildFont finalParamsList;
in
results
