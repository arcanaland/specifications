gate: toml abnf links

toml:
  ./tools/toml_check.py

abnf:
  ./tools/abnf_check.py

# fails on a dangling internal link
links:
  ./tools/build_pdf.py --check

pdf:
  ./tools/build_pdf.py

lint: abnf
