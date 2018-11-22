#include <stdio.h>
#include <stdlib.h>
int main()
{
    int row = 40;
    int col = 30;
    int *matrix_a_host;
    int *matrix_b_host;
    int *matrix_c_host;

    matrix_a_host = (int *)malloc(row*col*sizeof(int));
    matrix_b_host = (int *)malloc(row*col*sizeof(int));
    matrix_c_host = (int *)malloc(row*row*sizeof(int));
    for(int i = 0; i<row; i++)
    {
        for(int j = 0; j < col; j++)
        {
            matrix_a_host[i*col +j] = i+j;
        }
    }

    for(int i = 0; i<col; i++)
    {
        for(int j = 0; j < row; j++)
        {
            matrix_b_host[i*row +j] = i+j;
        }
    }
    for(int i= 0; i < row; i++)
    {
        for(int j = 0; j< row; j++)
        {
            int single_element = 0;
            for(int k = 0; k < col; k++)
            {
                single_element += matrix_a_host[i *col + k] * matrix_b_host[row* k + j];
            }
            matrix_c_host[row *i + j] = single_element;
            printf("%5d ", single_element);
        }
    }

    printf("\n-------------Matrix a-----------------\n");
    for(int i = 0; i < row*col; i++)
    {
        if((i + 1) % col)
            printf("%d ", *(matrix_a_host + i));
        else
            printf("%d \n", *(matrix_a_host + i));
    }
    printf("\n-------------Matrix b-----------------\n");
    for(int i = 0; i < row*col; i++)
    {
        if((i + 1) % row)
            printf("%d ", *(matrix_b_host + i));
        else
            printf("%d \n", *(matrix_b_host + i));
    }
    printf("\n-------------Matrix c-----------------\n");
    for(int i = 0; i < row*row; i++)
    {
        if((i + 1) % row)
            printf("%d ", *(matrix_c_host + i));
        else
            printf("%d \n", *(matrix_c_host + i));
    }
    free(matrix_a_host);
    free(matrix_b_host);
    free(matrix_c_host);
    return 1;
}
