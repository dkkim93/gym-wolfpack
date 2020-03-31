# gym-wolfpack
Implementation of the wolfpack domain as described in [`Leibo et al., AAMAS-17`](https://arxiv.org/pdf/1702.03037.pdf) (Multi-agent Reinforcement Learning in Sequential Social Dilemmas) with [`the OpenAI Gym toolkit`](https://gym.openai.com/)

## Dependency
Known dependencies are:
```
python (3.6.5)
pip (3.6)
virtualenv
```

## Setup
To avoid any conflict, please install Python virtual environment with [`virtualenv`](http://docs.python-guide.org/en/latest/dev/virtualenvs/):
```
pip3.6 install --upgrade virtualenv
```

## Run
After all the dependencies are installed, please run the code by running the following script.  
The script will start the virtual environment, install remaining Python dependencies in `requirements.txt`, and run the code.  
```
./_train.sh
```

## Result
The code should reproduce the following screenshot as the players are acting in the environment:
![alt text](https://github.com/dkkim93/gym-wolfpack/blob/master/screenshot.png)
