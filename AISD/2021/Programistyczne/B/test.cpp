#include<cstdio>

int previous_index[51][1001], val[51], n;

bool chk[51];

int abs(int a){ return a>0?a:-a; }

void fill_table_with_minus_one(int n,int sum){
    for(int i=1;i<=n;i++)
        for(int s=0;s<=sum;s++)
            previous_index[i][s] = -1;
}

void fill_table(int ind, int sum_till_ind_minus_one, int last_summed){
    if(ind > n) return;
    if(previous_index[ind][sum_till_ind_minus_one] != -1) return;
    fill_table(ind+1, sum_till_ind_minus_one, last_summed);
    previous_index[ind][sum_till_ind_minus_one + val[ind]] = last_summed;
    fill_table(ind+1, sum_till_ind_minus_one + val[ind], ind);
}

int main(){
    int sum=0;
    scanf("%d",&n);
    for(int i=1;i<=n;i++){
        scanf("%d",&val[i]);
        sum += val[i];
    }
    fill_table_with_minus_one(n,sum);
    fill_table(1,0,0);
    int saveind=0,saveval=0;
    for(int local_sum = 0;local_sum <= sum/2; local_sum++)
        for(int i=1;i<=n;i++)
            if(previous_index[i][local_sum] != -1){
                saveind = i;
                saveval = local_sum;
            }
    while(saveind > 0){
        printf("%d %d\n",saveind, saveval);
        chk[saveind] = 1;
        int temp = val[saveind];
        saveind = previous_index[saveind][saveval];
        saveval -= temp;
    }
    for(int i=1;i<=n;i++)
        if(chk[i]) 
            printf("%d ",val[i]);
    printf("\n");
    for(int i=1;i<=n;i++)
        if(!chk[i])
            printf("%d ",val[i]);
}