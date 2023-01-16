rm coex.zip
yes | zip -r coex.zip COEX_*/*K/{COLVAR,DELTAFS} 
scp  coex.zip hopper:projects/DeepMDPhaseDiagram/4-PhaseDiagram/IceII-Liquid/5-BiasedCoexistence_3rd
ssh hopper 'cd /home/sbore/projects/DeepMDPhaseDiagram/4-PhaseDiagram/IceII-Liquid/5-BiasedCoexistence_3rd;
yes|unzip coex.zip;
ipython --TerminalIPythonApp.file_to_run=  AnalyzeCoexistence.ipynb
'
