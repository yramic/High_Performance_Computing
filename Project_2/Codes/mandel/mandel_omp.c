#include <stdio.h>
#include <stdlib.h>
#include <omp.h> // Add OpenMP Library!

#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#include "consts.h"
#include "pngwriter.h"
#include "walltime.h"

int main(int argc, char **argv) {
  png_data *pPng = png_create(IMAGE_WIDTH, IMAGE_HEIGHT);

  double x, y, x2, y2, cx, cy, x_temp;

  double fDeltaX = (MAX_X - MIN_X) / (double)IMAGE_WIDTH;
  double fDeltaY = (MAX_Y - MIN_Y) / (double)IMAGE_HEIGHT;

  long nTotalIterationsCount = 0;

  long i, j, n;
  int c;

  int threads = 4; // Initialize the number of threads with 1!
  if (argc > 1) threads = atol(argv[1]); // update the number of threads
  omp_set_num_threads(threads);

  double time_start = walltime();

  #pragma omp parallel private(c,cx,cy,x,y,x2,y2,n,i,j) shared(nTotalIterationsCount, fDeltaX,fDeltaY,pPng)
  {
  #pragma omp for
       for (j = 0; j < IMAGE_HEIGHT; j++) {

              cy = MIN_Y + j*fDeltaY;

              for (i = 0; i < IMAGE_WIDTH; i++) {

                     cx = MIN_X + i*fDeltaX;

                     // compute the orbit z, f(z), f^2(z), f^3(z), ...
                     // count the iterations until the orbit leaves the circle |z|=2.
                     // stop if the number of iterations exceeds the bound MAX_ITERS.
                     n = 0;
                     // TODO
                     // >>>>>>>> CODE IS MISSING
                     x = 0;
                     y = 0;
                     x2 = 0;
                     y2 = 0;
                     do {
                            x_temp = x*x - y*y + cx;
                            y = 2*x*y + cy;
                            x = x_temp;
                            // Update x2 and y2!
                            x2 = x * x;
                            y2 = y * y;
                            n++;
                     } while ((x2 + y2 < 2*2) && n < MAX_ITERS); // <= or < ????

                     #pragma omp atomic
                            nTotalIterationsCount += n;

                     // <<<<<<<< CODE IS MISSING
                     // n indicates if the point belongs to the mandelbrot set
                     // plot the number of iterations at point (i, j)
                     c = ((long)n * 255) / MAX_ITERS;
                     png_plot(pPng, i, j, c, c, c);
              }
       }
  } // END OMP!
  double time_end = walltime();

  // print benchmark data
  printf("Total time:                 %g seconds\n",
         (time_end - time_start));
  printf("Image size:                 %ld x %ld = %ld Pixels\n",
         (long)IMAGE_WIDTH, (long)IMAGE_HEIGHT,
         (long)(IMAGE_WIDTH * IMAGE_HEIGHT));
  printf("Total number of iterations: %ld\n", nTotalIterationsCount);
  printf("Avg. time per pixel:        %g seconds\n",
         (time_end - time_start) / (double)(IMAGE_WIDTH * IMAGE_HEIGHT));
  printf("Avg. time per iteration:    %g seconds\n",
         (time_end - time_start) / (double)nTotalIterationsCount);
  printf("Iterations/second:          %g\n",
         nTotalIterationsCount / (time_end - time_start));
  // assume there are 8 floating point operations per iteration
  printf("MFlop/s:                    %g\n",
         nTotalIterationsCount * 8.0 / (time_end - time_start) * 1.e-6);

  png_write(pPng, "mandel.png");
  return 0;
}
