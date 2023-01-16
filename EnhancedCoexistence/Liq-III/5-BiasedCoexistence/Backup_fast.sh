rm coex.zip
yes | zip -r coex.zip COEX_*/*K/{COLVAR,DELTAFS} 
scp  coex.zip hopper:/home/sbore/projects/DeepMDPhaseDiagram/4-PhaseDiagram/IceIII-Liquid/5-BiasedCoexistence/
ssh hopper 'cd /home/sbore/projects/DeepMDPhaseDiagram/4-PhaseDiagram/IceIII-Liquid/5-BiasedCoexistence;
yes|unzip coex.zip;
ipython --TerminalIPythonApp.file_to_run=  AnalyzeCoexistence.ipynb
'
