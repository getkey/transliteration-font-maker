{ pkgs ? import <nixpkgs> {}, version }:

let
  pkgs = import <nixpkgs> {};
  buildFont = import ./build_font.nix;
  transliterations = [
    "traditional_greek_romanization"
    "iso_9_1995"
  ];
  paramsList = builtins.map (transliteration: { inherit transliteration; version = version; }) transliterations;
  results = builtins.map buildFont paramsList;
in
results
