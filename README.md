# priceisright
Monte Carlo simulation of "The Price is Right" odds of the first spinner winning at the big wheel

Usage:
  python bigwheel.py [-n ITERATIONS] [-x] [-p plotfile.png]

  Output:  CSV file or PNG file with "-p plotfile.png" option

  --xkcd or -x combined with --plot/-p filename.png will produce a
    plot of the results in the format of plots from xkcd.com

initial roll, odds of winning by staying, odds of winning by spinning again

Usage:
  python who_wins.py [--iterations/-n number of iterations]
                     [--player-1-threshold/-2 P1Threshold]
                     [--player-2-threshold/-2 P2Threshold]
                     [--plot/-p plotfile.png]
                     [--xkcd/-x]
  Output:  CSV file or PNG file with "-p plotfile.png" option for who
  of the three "Price is Right" players wins.
