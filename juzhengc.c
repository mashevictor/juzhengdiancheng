#include <stdio.h>
int main ()
{	int arr_a[4][2]={4,5,6,9,8,7,10,8};//a是4行2列	
	int arr_b[2][4]={3,2,1,6,5,4,11,23};//b是2行4列
        int i,j,k;
	int row_a=sizeof(arr_a)/sizeof(arr_a[0]);
	int col_a=sizeof(arr_a[0])/sizeof(arr_a[0][0]);
    	printf("行数：%d 列数：%d\n",row_a,col_a);
	int arr_res[4][4]={0};//最终点乘生成的数列是：行数等于A的行数，列数等于B的列数
	
        for(i = 0; i < 4; i++)//这个是新数列的行
        {
                for(j = 0; j <4; j++)//这个是新数列的列
                {
			int sum=0;
                        for(k = 0; k < 2; k++)//这个k是A数列的列
                        {
                		sum = sum + arr_a[i][k] * arr_b[k][j];
                        }
                arr_res[i][j] = sum;
                printf("%5d ", arr_res[i][j]);
                }
        }

}


