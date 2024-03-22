#include <stdio.h>
#include <stdlib.h>
#include "walltime.h"
#include <omp.h>

void print_list(double *data, int length) {
  for (int i = 0; i < length; i++) {
    printf("%e\t", data[i]);
  }
  printf("\n");
}

void quicksort(double *data, int length) {
  if (length <= 1) return;

  // print_list(data, length);

  double pivot = data[0];
  double temp;
  int left = 1;
  int right = length - 1;

  do {
    while (left  < (length - 1) && data[left ] <= pivot) left++ ;
    while (right > 0            && data[right] >= pivot) right--;

    /* swap elements */
    if (left < right) {
      temp = data[left];
      data[left ] = data[right];
      data[right] = temp;
    }
  } while (left < right);

  if (data[right] < pivot) {
    data[0] = data[right];
    data[right] = pivot;
  }

  // print_list(data, length);

  /* recursion */
 
#pragma omp task firstprivate(data, right)
{
  quicksort(data, right);
}
#pragma omp task firstprivate(data, length, left)
{
  quicksort(&(data[left]), length - left);
}

// #pragma omp parallel sections
// { 
// #pragma omp section
//   {
//     quicksort(data, right);
//   }
// #pragma omp section
//   {
//     quicksort(&(data[left]), length - left);
//   }
// }
}

int check(double *data, int length) {
  for (int i = 1; i < length; i++) {
    if (data[i] < data[i-1]) return 1;
  }
  return 0;
}

int main(int argc, char **argv) {
  int length;
  double *data;

  int mem_size;

  int i, j, k;

  length = 10000000;
  if (argc > 1) length = atoi(argv[1]);

  data = (double*)malloc(length * sizeof(double));
  if (data == NULL) {
    printf("memory allocation failed");
    return 0;
  }

  /* initialisation */
  srand(0);
  for (i = 0; i < length; i++) {
    data[i] = (double)rand() / (double)RAND_MAX;
  }

  // print_list(data, length);

  
  // print_list(data, length);
  // Do the experiment several times and then take the average!
  // int n_exp = 3; // Number of experiments!
  // // Allocate memory to store all Times!
  // double *times;
  // times = malloc(n_exp * sizeof (double));

  // for (int i = 0; i < (n_exp-1); i++) {
  //   // Start Algorithm here!
  //   double time_start = walltime();
  //   #pragma omp parallel shared(data, length)
  //   {
  //   #pragma omp single nowait
  //     {
  //       quicksort(data, length);
  //     }
  //   }
  //   double time = walltime() - time_start;

  //   // Store the times!
  //   times[i] = time;
  // }
  // double avg_time = 0;
  // for (int idx = 0; idx < n_exp-1; idx++){
  //   avg_time += times[idx];
  // }
  // avg_time /= n_exp;
  // print_list(data, length);

  double time_start = walltime();
  #pragma omp parallel shared(data, length)
  {
  #pragma omp single nowait
    {
      quicksort(data, length);
    }
  }
  double time = walltime() - time_start;

  // print_list(data, length);

  printf("Size of dataset: %d, elapsed time[s] %e \n", length, time);

  // printf("Size of dataset: %d, elapsed time[s] %e \n", length, avg_time);

  if (check(data, length) != 0) printf("Quicksort incorrect.\n");

  return 0;
}