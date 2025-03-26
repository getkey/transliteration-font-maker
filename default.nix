{ pkgs ? import <nixpkgs> {}, version }:

let
	pkgs = import <nixpkgs> {};
	buildFont = import ./build_font.nix;
	transliterations = [
		"iso_9_1995"
		"traditional_greek_romanization"
	];
	paramsList = builtins.map (transliteration: { inherit transliteration; version = version; }) transliterations;
	results = builtins.map buildFont paramsList;
in
results
