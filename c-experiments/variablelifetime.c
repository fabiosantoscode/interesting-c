
int *give_int(){
    int *i = (int*)malloc(sizeof(int));
    *i = 3;
    
    return i;
}

int main(){
    int i = *give_int();
    printf("%d\n", i);
    return 0;
}


