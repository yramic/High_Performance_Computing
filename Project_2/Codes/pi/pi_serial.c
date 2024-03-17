#include <stdio.h> /* printf */
#include <stdlib.h> /* atol */
#include "walltime.h"

int main(int argc, char *argv[]) {
  long int N = 1000000;
  double time_start, h, sum, pi;

  if ( argc > 1 ) N = atol(argv[1]);

  double time_tot = 0.0;
  double avg_time = 0.0;
  // To the experiment 10 times and build the average!
  for (int experiment = 0; experiment < 10; ++experiment) {
    time_start = walltime();
    h = 1./N;
    sum = 0.;
    for (int i = 0; i < N; ++i) {
      double x = (i + 0.5)*h;
      sum += 4.0 / (1.0 + x*x);
    }
    pi = sum*h;
    double time = walltime() - time_start;
    time_tot += time;
  }

  avg_time = time_tot/10;

  // printf("pi = \%.15f, N = %9ld, time = %.8f secs\n", pi, N, avg_time);
  printf("\%.15f,%ld,%.8f\n", pi, N, avg_time);

  return 0;
}
