# Bike Sharing Dashboard

## Setup Environment - Anaconda
```
mkdir -p ~/miniconda3
curl -o ~/miniconda3/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init zsh
source ~/.zshrc

conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```