// #pragma omp simd
// #pragma unroll

const char* dgemm_desc = "Blocked dgemm.";

/* This routine performs a dgemm operation
 *
 *  C := C + A * B
 *
 * where A, B, and C are lda-by-lda matrices stored in column-major format.
 * On exit, A and B maintain their input values.
 */
// #pragma omp parallel for private(i,j,k) shared(A,B,C)
// #define BLOCK_SIZE 24
void square_dgemm(int n, double* restrict A, double* restrict B, double* restrict C) {
  // TODO: Implement the blocking optimization

  // ----------------------- Matrix Blocking -------------------------
  int BLOCK_SIZE = 26; // 36 is the theoretical max value!
  #pragma omp parallel for collapse(2)
  for (int k = 0; k < n; k += BLOCK_SIZE) {
    for (int j = 0; j < n; j += BLOCK_SIZE) {
        for (int i = 0; i < n; i += BLOCK_SIZE) {
            // Matrix Multiplication here!
            for (int idx_k = k; idx_k < k + BLOCK_SIZE && idx_k < n; ++idx_k)  {
                for (int idx_j = j; idx_j < j + BLOCK_SIZE && idx_j < n; ++idx_j) {
                    // double sum = 0.0;
                    #pragma unroll
                    for (int idx_i = i; idx_i < i + BLOCK_SIZE && idx_i < n; ++idx_i){
                      #pragma omp atomic
                      C[idx_i + idx_j * n] += A[idx_i + idx_k * n] * B[idx_k + idx_j * n];
                        // sum += A[idx_i + idx_k * n] * B[idx_k + idx_j * n];
                    }
                    // C[idx_i + idx_j * n] += sum;
                }
            }
        }
    }
  }

  // ----------------------- Optimized Naive Implementation -------------------------
  // Naive Implementation but with a change of the loop order, gave me better results than
  // the Matrix Blocking / Tiling!

  // for (int k = 0; k < n; ++k) {
  //   for (int j = 0; j < n; ++j) {
  //     // #pragma unroll
  //     for(int i = 0; i < n; ++i) {
  //       // #pragma omp atomic
	//       C[i+j*n] += A[i+k*n] * B[k+j*n];
  //     }
  //   }
  // }

  // ----------------------- Summary -------------------------
  // The matrix blocking approach gave me at best restuls around 24.71%, while the optimized naive implementation outperforms
  // the matrix blocking optimization and reached results above 27%!

}
