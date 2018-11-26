#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import pycuda.driver as cuda
import pycuda.autoinit
import pycuda.gpuarray as gpuarray
import multiprocessing as mp
import threading as td
import time
import numpy as np
import math
import cmath
np.set_printoptions(suppress=True)

def normal():
    shuzu = np.random.randn(4000,4000).astype(np.float32)
    shuzu2 = np.random.randn(4000,4000).astype(np.float32)
    he=np.dot(shuzu,shuzu2)
    print(he)
    return he

import numpy as np
from numpy import linalg as la
from pycuda import driver, compiler, gpuarray, tools

# -- initialize the device
import pycuda.autoinit

kernel_code_template = """
__global__ void MatrixMulKernel(float *A, float *B, float *C)
{

  const uint wA = %(MATRIX_SIZE)s;
  const uint wB = %(MATRIX_SIZE)s;  
  
  // Block index
  const uint bx = blockIdx.x;
  const uint by = blockIdx.y;

  // Thread index
  const uint tx = threadIdx.x;
  const uint ty = threadIdx.y;

  // Index of the first sub-matrix of A processed by the block
  const uint aBegin = wA * %(BLOCK_SIZE)s * by;
  // Index of the last sub-matrix of A processed by the block
  const uint aEnd = aBegin + wA - 1;
  // Step size used to iterate through the sub-matrices of A
  const uint aStep = %(BLOCK_SIZE)s;

  // Index of the first sub-matrix of B processed by the block
  const uint bBegin = %(BLOCK_SIZE)s * bx;
  // Step size used to iterate through the sub-matrices of B
  const uint bStep = %(BLOCK_SIZE)s * wB;

  // The element of the block sub-matrix that is computed
  // by the thread
  float Csub = 0;
  // Loop over all the sub-matrices of A and B required to
  // compute the block sub-matrix
  for (int a = aBegin, b = bBegin;
       a <= aEnd;
       a += aStep, b += bStep) 
    {
      // Shared memory for the sub-matrix of A
      __shared__ float As[%(BLOCK_SIZE)s][%(BLOCK_SIZE)s];
      // Shared memory for the sub-matrix of B
      __shared__ float Bs[%(BLOCK_SIZE)s][%(BLOCK_SIZE)s];

      // Load the matrices from global memory to shared memory
      // each thread loads one element of each matrix
      As[ty][tx] = A[a + wA * ty + tx];
      Bs[ty][tx] = B[b + wB * ty + tx];
      // Synchronize to make sure the matrices are loaded
      __syncthreads();

      // Multiply the two matrices together;
      // each thread computes one element
      // of the block sub-matrix
      for (int k = 0; k < %(BLOCK_SIZE)s; ++k)
        Csub += As[ty][k] * Bs[k][tx];

      // Synchronize to make sure that the preceding
      // computation is done before loading two new
      // sub-matrices of A and B in the next iteration
      __syncthreads();
    }

  // Write the block sub-matrix to global memory;
  // each thread writes one element
  const uint c = wB * %(BLOCK_SIZE)s * by + %(BLOCK_SIZE)s * bx;
  C[c + wB * ty + tx] = Csub;
}
"""

def zuikuai():
    MATRIX_SIZE = 4000

# define size of blocks and tiles sub-matrix 
# (we assume that the block size is same as tile size)
    TILE_SIZE = 2
    BLOCK_SIZE = TILE_SIZE

# create two random square matrices
#a_cpu = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float32)
#b_cpu = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float32)
    a_cpu = np.random.randn(4000,4000).astype(np.float32)
    b_cpu = np.random.randn(4000,4000).astype(np.float32)


# transfer host (CPU) memory to device (GPU) memory
    #st_zuikuai = time.time()
    a_gpu = gpuarray.to_gpu(a_cpu) 
    b_gpu = gpuarray.to_gpu(b_cpu)

# create empty gpu array for the result (C = A * B)
    c_gpu = gpuarray.empty((MATRIX_SIZE, MATRIX_SIZE), np.float32)

# get the kernel code from the template 
# by specifying the constants MATRIX_SIZE and BLOCK_SIZE
    kernel_code = kernel_code_template % { 
    'MATRIX_SIZE': MATRIX_SIZE,
    'BLOCK_SIZE': BLOCK_SIZE,
    }

# compile the kernel code
    mod = compiler.SourceModule(kernel_code)

# get the kernel function from the compiled module
    matrixmul = mod.get_function("MatrixMulKernel")

# call the kernel on the card
    matrixmul(
    # inputs
    a_gpu, b_gpu, 
    # output
    c_gpu, 
    # grid of multiple blocks
    grid = (MATRIX_SIZE // TILE_SIZE, MATRIX_SIZE // TILE_SIZE),
    # block of multiple threads
    block = (TILE_SIZE, TILE_SIZE, 1), 
    )

    #st1_zuikuai= time.time()
    #print('zuikuai time:', st1_zuikuai - st_zuikuai) 


st = time.time()
normal()
st1= time.time()
print('normal time:', st1-st)
#zuikuai()
st2 = time.time()
zuikuai()
st2end= time.time()
print('normal2 time:', st2end-st2)
