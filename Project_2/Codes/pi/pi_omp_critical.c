#include <stdio.h> /* printf */
#include <stdlib.h> /* atol */
#include "walltime.h"
#include "omp.h"


int main(int argc, char *argv[]) {
  long int N = 1000000;
  int threads = 4;
  double time_start, h, sum, pi;

  if ( argc > 1 ) N = atol(argv[1]);

  if ( argc > 2 ) threads = atol(argv[2]);

  double time_tot = 0.0;
  double avg_time = 0.0;
  // To the experiment 10 times and build the average!
  for (int experiment = 0; experiment < 10; ++experiment) {
    /* Parallelize with OpenMP using the critical directive */
    time_start = walltime();
    h = 1./N;
    sum = 0.;
    // omp_set_num_threads(NUM_THREADS);
    omp_set_num_threads(threads);
    #pragma omp parallel
    {
      double partial_sum = 0.;
      int nthreads = omp_get_num_threads();
      int tid = omp_get_thread_num();
      int i_beg = tid * N / nthreads;
      int i_end = (tid + 1) * N / nthreads;
      for (int i = i_beg; i < i_end; ++i) {
        double x = (i + 0.5)*h;
        partial_sum += 4.0 / (1.0 + x*x);
      }
      #pragma omp critical
        sum += partial_sum;
    } // Parallelization ends here!
    pi = sum*h;
    double time = walltime() - time_start;

    time_tot += time;
  }
  avg_time = time_tot / 10;

  // printf("pi = \%.15f, N = %9ld, threads = %2d, time = %.8f secs\n", pi, N, threads, avg_time);
  printf("\%.15f,%ld,%d,%.8f\n", pi, N, threads, avg_time);

  return 0;
}