1. This project solves the Traveling Salesman Problem using Simulated Annealing and a Genetic Algorithm.

2. The run command is python3 tspOptim.py
    a. Have to have python3 & matplotlib
    b. pip install matplotlib --break-system-packages

3. Example output:
python3 tspOptim.py
Nearest-neighbor length: 6.0214
/home/branos/csci580/tspOptim.py:86: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
  plt.show()
[SA] iter=  2000 T=0.07356 cur=8.3800 best=6.0214
[SA] iter=  4000 T=0.02705 cur=6.5972 best=6.0214
[SA] iter=  6000 T=0.00995 cur=5.3139 best=5.3139
[SA] iter=  8000 T=0.003659 cur=5.0057 best=5.0057
[SA] iter= 10000 T=0.001346 cur=5.0057 best=5.0057
[SA] iter= 12000 T=0.000495 cur=5.0057 best=5.0057
[SA] iter= 14000 T=0.0001821 cur=5.0057 best=5.0057
[SA] iter= 16000 T=6.696e-05 cur=5.0057 best=5.0057
[SA] iter= 18000 T=2.463e-05 cur=5.0057 best=5.0057
[SA] iter= 20000 T=9.057e-06 cur=5.0057 best=5.0057
SA best length: 5.0057
SA improvement vs NN: 16.87%
/home/branos/csci580/tspOptim.py:94: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
  plt.show()
[GA] gen= 100 best=5.9001
[GA] gen= 200 best=5.9001
[GA] gen= 300 best=5.9001
[GA] gen= 400 best=5.8049
[GA] gen= 500 best=5.7995
[GA] gen= 600 best=5.7995
[GA] gen= 700 best=5.6298
[GA] gen= 800 best=5.3886
[GA] gen= 900 best=5.3886
[GA] gen=1000 best=5.3621
GA best length: 5.3621
GA improvement vs NN: 10.95%
/home/branos/csci580/tspOptim.py:109: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
  plt.show()
NN: 6.0214 | SA: 5.0057 | GA: 5.3621
SA length: 5.0057 | Improvement vs NN: 16.87%
✅ SA passed improvement threshold!
GA length: 5.3621 | Improvement vs NN: 10.95%
✅ GA passed improvement threshold!