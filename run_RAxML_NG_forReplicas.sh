cp out/incomplete/$1/astral/$2"_gt_species.out.tre" input.nwk
cp out/incomplete/$1/gt/$2"_gt.tre" gt.tre
jupyter nbconvert --to script processor.ipynb
python processor.py
./bin/raxml-ng input.nwk input.data