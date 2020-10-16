# SEISPY

Simplified tools to manage seismic traces  
* Store, filter, manipulate seismic waveforms  
* Visualise array data based on matplotlib collections  
* Very light dependencies : numpy + scipy + matplotib
* Save and load seismic data using numpy npz format (system independent)
* No dependency to obspy, although conversion from obspy is handled

Download 
```
cd $INSTALLPATH
conda clone https://github.com/obsmax/seispy.git
```

Create the environment
```
conda create -n sp python=3.7 --yes
conda activate sp
```

Install (editable mode)
```
cd $INSTALLPATH/seispy
pip install -e .
```