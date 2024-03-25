#include "walltime.h"
#include <iostream>
#include <random>
#include <vector>
#include <omp.h>

#define VEC_SIZE 1000000000
#define BINS 16

int main() {
  double time_start, time_end;

  // Initialize random number generator
  unsigned int seed = 123;
  float mean = BINS / 2.0;
  float sigma = BINS / 12.0;
  std::default_random_engine generator(seed);
  std::normal_distribution<float> distribution(mean, sigma);

  // Generate random sequence
  // Note: normal distribution is on interval [-inf; inf]
  //       we want [0; BINS-1]
  std::vector<int> vec(VEC_SIZE);
  for (long i = 0; i < VEC_SIZE; ++i) {
    vec[i] = int(distribution(generator));
    if (vec[i] < 0       ) vec[i] = 0;
    if (vec[i] > BINS - 1) vec[i] = BINS - 1;
  }

  // Initialize histogram: Set all bins to zero
  long dist[BINS];
  for (int i = 0; i < BINS; ++i) {
    dist[i] = 0;
  }

  // TODO Parallelize the histogram computation
  // Note c-style array, integer with stacksize BIN is created, not a pointer!
  long dist_local[BINS];
  for (int bin = 0; bin < BINS; ++bin) {
    dist_local[bin] = 0;
  }

  time_start = walltime();
  // TODO Parallelize the histogram computation
  #pragma omp parallel shared(vec, dist) firstprivate(dist_local)
  {
    // For some reason dist_local has to be defined inside the omp area
    // otherwise I will get racing issues and I end up having wrong results!
    // long dist_local[BINS];
    // for (int bin = 0; bin < BINS; ++bin) {
    //   dist_local[bin] = 0;
    // }

  #pragma omp for
    for (long i = 0; i < VEC_SIZE; ++i) {
      dist_local[vec[i]]++;
    }
    
    for (int bin = 0; bin < BINS; ++bin) {
  #pragma omp atomic
      dist[bin] += dist_local[bin];
    }
  }
  time_end = walltime();

  // Write results
  for (int i = 0; i < BINS; ++i) {
    std::cout << "dist[" << i << "]=" << dist[i] << std::endl;
  }
  std::cout << "Time: " << time_end - time_start << " sec" << std::endl;

  return 0;
}
