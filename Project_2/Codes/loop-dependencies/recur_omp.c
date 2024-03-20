#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "walltime.h"
#include <omp.h>

int main(int argc, char *argv[]) {
  int N = 2000000000;
  double up = 1.00000001;
  double Sn = 1.00000001;
  int n;

  /* allocate memory for the recursion */
  double *opt = (double *)malloc((N + 1) * sizeof(double));
  if (opt == NULL) {
    perror("failed to allocate problem size");
    exit(EXIT_FAILURE);
  }

  int lastn = -2;

  double time_start = walltime();
  // TODO: YOU NEED TO PARALLELIZE THIS LOOP
  #pragma omp parallel shared(opt) private(n)
  {
  #pragma omp for firstprivate(lastn) lastprivate(Sn)
    for (n = 0; n <= N; ++n) {
      if (lastn == n - 1) {
        // If I am not at the first step, use the fast version!
        Sn *= up;
      } else {
        // If at the start: use the slow version!
        // Note that S0 = up!
        Sn = up * pow(up, n);
      }
      opt[n] = Sn;
      // Update lastn!
      lastn = n; // From now on only the fast version will be used!
    }
  }

  printf("Parallel RunTime  :  %f seconds\n", walltime() - time_start);
  printf("Final Result Sn   :  %.17g \n", Sn);

  double temp = 0.0;
  for (n = 0; n <= N; ++n) {
    temp += opt[n] * opt[n];
  }
  printf("Result ||opt||^2_2 :  %f\n", temp / (double)N);
  printf("\n");

  return 0;
}
