# Prisoner's Riddle
Simulate the [prisoner's riddle](https://www.youtube.com/watch?v=iSNsgj1OCLA).

## Run the Simulation

Open terminal and clone the repository. Navigate to that directory, create a virtual environment and install requirements:
```
$ git clone https://github.com/davidherook/prisoners-riddle.git
$ cd prisoners-riddle
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the simulation defining the number of `--rounds` and `--prisoners`. You will see the results printed to the screen. Results for each round will be saved to a folder named `results`.

```
$ python simulation.py --rounds 1000 --prisoners 100

**************************************************

Simulating 1000 rounds with 100 prisoners each round...
Saved results to results/results_1671828090.csv

Results Summary:

Prisoners per Round 100
Rounds Simulated 1000
Rounds Successful 314
% Success 0.314

**************************************************
```