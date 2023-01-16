ls */*Biased*/AnalyzeCoexistence.ipynb  | xargs -l bash -c 'cp StandardIpynbFiles/AnalyzeCoexistence.ipynb $0'

# find Ice*-Liquid*/*Biased*/* -name *.json | xargs -l bash -c ' sed -i "s/fig1_size.*/fig1_size\": [12,7],/g" $0'
# find Ice*-Liquid*/*Biased*/* -name *.json | xargs -l bash -c ' sed -i "s/fig2_size.*/fig2_size\": [7,5],/g" $0'


# find IceII-Liquid/*Biased*/* -name *.json | xargs -l bash -c ' sed -i "s/fig1_size.*/fig1_size\": [12,6.5],/g" $0'
# find IceII-Liquid/*Biased*/* -name *.json | xargs -l bash -c ' sed -i "s/fig2_size.*/fig2_size\": [7,4.5],/g" $0'
